import hashlib

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from typing import Optional, Literal
from sqlalchemy.orm import Session

from app.db.model.user import UserModel, EmailVerification
from app.deps import get_db, hash_password
from app.services.email import prepare_verification_link, send_mail_verification
from app.setup.limiter import limiter

router = APIRouter()


class MailVerifyRequest(BaseModel):
    type: Literal["registration", "forgot_pass", "email_change"]
    token: str
    new_password: Optional[str] = None
    new_email: Optional[str] = None

@router.post("/verify", description="[FROZEN] Mail verification endpoint")
def verify_mail(
    payload: MailVerifyRequest,
    db: Session = Depends(get_db),
):
    # token setup
    verification = None
    token_hash = hashlib.sha256(payload.token.encode()).hexdigest()
    verification = db.query(EmailVerification).filter(
        EmailVerification.token_hash==token_hash, EmailVerification.token_type==payload.type
    ).first()

    if not verification:
        raise HTTPException(
            status_code=404, 
            detail="This verification link is invalid!\nPlease request a new verification email."
        )
    if verification.used: 
        raise HTTPException(
            status_code=410, 
            detail="This verification link has already been used."
        )
    
    user = (db.query(UserModel).filter(UserModel.email==verification.email).first())
    if user is None or not user.is_active:
        raise HTTPException(status_code=404, detail="Account not found.")

    if verification.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=410, detail="This verification link has expired!\nPlease request a new verification email.")

    response = None

    if payload.type == "registration":
        user.is_verified = True
        verification.used = True
        response = "Email verified successfully."

    elif payload.type == "forgot_pass":
        if payload.new_password:
            user.password = hash_password(payload.new_password)
            verification.used = True
            response = "Password reset"
        else:
            raise HTTPException(status_code=400, detail="Please provide a new password.")

    elif payload.type == "email_change":
        if payload.new_email:
            user.email = payload.new_email
            verification.used = True
            response = "Your email address has been updated successfully."
        else:
            raise HTTPException(status_code=400, detail="Please provide a new email address.")
        
    else:
        raise HTTPException(status_code=400, detail="Invalid verification request.")
    
    db.commit()

    print(f"[VERIFY] email={verification.email} type={payload.type} used={verification.used}")
    return JSONResponse(status_code=200, content= {"detail": response})


class ResendMailRequest(BaseModel):
    email: str

@router.post("/resend", description="[FROZEN] Mail resend endpoint")
@limiter.limit('5/minute')   # allow max 5 requests per minute per IP
def resend_mail(
    request: Request,
    payload: ResendMailRequest,
    db: Session = Depends(get_db),
):
    user = db.query(UserModel).filter(UserModel.email==payload.email).first()

    if not user or not user.is_active: 
        raise HTTPException(status_code=404, detail="Account not found.")
    
    if user.is_verified: 
        raise HTTPException(status_code=409, detail="This email is already verified.")

    link = prepare_verification_link(db=db, email=payload.email, token_type="registration")
    send_mail_verification(payload.email, link)
    return JSONResponse(status_code=200, content= {"detail": "Verification email sent. Please check your inbox."})

