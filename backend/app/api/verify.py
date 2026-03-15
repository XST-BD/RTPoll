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

@router.post("/verify", description="Mail verification endpoint")
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
            detail="Invalid link!\nPlease resend the email to receive a new one."
        )
    if verification.used: 
        raise HTTPException(
            status_code=410, 
            detail="Link is already used!\nPlease resend the email to receive a new one."
        )
    
    user = (db.query(UserModel).filter(UserModel.email==verification.email).first())
    if user is None or not user.is_active:
        raise HTTPException(status_code=404, detail="User not found")

    if verification.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=410, detail="Link has expired")

    response = None

    if payload.type == "registration":
        user.is_verified = True
        verification.used = True
        response = "Verification successful"

    elif payload.type == "forgot_pass":
        if payload.new_password:
            user.password = hash_password(payload.new_password)
            verification.used = True
            response = "Password reset"
        else:
            raise HTTPException(status_code=400, detail="No new password provided")

    elif payload.type == "email_change":
        if payload.new_email:
            user.email = payload.new_email
            verification.used = True
            response = "Email reset"
        else:
            raise HTTPException(status_code=400, detail="No new email provided")
        
    else:
        raise HTTPException(status_code=400, detail="Unknown type")
    
    db.commit()

    print(f"[VERIFY] email={verification.email} type={payload.type} used={verification.used}")
    return JSONResponse(status_code=200, content= {"detail": response})


class ResendMailRequest(BaseModel):
    email: str

@router.post("/resend", description="Mail resend endpoint")
@limiter.limit('5/minute')   # allow max 5 requests per minute per IP
def resend_mail(
    request: Request,
    payload: ResendMailRequest,
    db: Session = Depends(get_db),
):
    user = db.query(UserModel).filter(UserModel.email==payload.email).first()

    if not user or not user.is_active: 
        raise HTTPException(status_code=404, detail="User not found during mail validation")
    
    if user.is_verified: 
        raise HTTPException(status_code=409, detail="User already verified")

    link = prepare_verification_link(db=db, email=payload.email, token_type="registration")
    send_mail_verification(payload.email, link)
    return JSONResponse(status_code=200, content= {"detail": "Mail verification sent"})

