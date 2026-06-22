import hashlib

from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from app.db.model.user import UserModel, EmailVerification
from app.deps import get_db, hash_password
from app.services.email import prepare_verification_link, send_mail_verification
from app.setup.limiter import limiter
from app.setup.vars import ENV
from app.utils.db import delete_hard
from app.utils.email import validate_email

router = APIRouter()


class MailVerifyRequest(BaseModel):
    token: str
    new_password: Optional[str] = None

@router.post("/verify", description="[FROZEN] Mail verification endpoint")
def verify_mail(
    payload: MailVerifyRequest,
    db: Session = Depends(get_db),
):
    # token setup
    verification = None
    token_hash = hashlib.sha256(payload.token.encode()).hexdigest()
    verification = db.query(EmailVerification).filter(EmailVerification.token_hash==token_hash).first()

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
    
    if verification.extra_data: 
        user = (db.query(UserModel).filter(UserModel.email==verification.extra_data).first())
    else: 
        user = (db.query(UserModel).filter(UserModel.email==verification.email).first())
        if user is None or not user.is_active:
            raise HTTPException(status_code=404, detail="Account not found.")

    # if verification.expires_at < datetime.now(timezone.utc):
    #     raise HTTPException(status_code=410, detail="This verification link has expired!\nPlease request a new verification email.")

    response = None

    if user and verification.token_type == "registration":
        user.is_verified = True
        verification.used = True
        response = JSONResponse(
                status_code=200, 
                content= {"detail": "Email verified successfully."}
            )

    elif user and verification.token_type == "forgot_pass":
        if payload.new_password:

            if len(payload.new_password) < 8:
                raise HTTPException(status_code=406, detail="Password must contain at least 8 characters.")

            user.password = hash_password(payload.new_password)
            verification.used = True
            response = JSONResponse(
                status_code=200, 
                content= {"detail": "Password updated successfully."}
            )
        else:
            raise HTTPException(status_code=400, detail="Please provide a new password.")

    elif user and verification.token_type == "email_change":
        if verification.email:

            if not validate_email(verification.email):
                raise HTTPException(status_code=406, detail="Please enter a valid email address.")
            
            # Hard deletion if new mail was previously used
            # sqlite uses ? as placeholder while psql uses %s
            delete_hard("users", "email=%s", (verification.email,))

            user.email = verification.email
            verification.used = True
            response = JSONResponse(
                status_code=200, 
                content= {"detail": "Your email address has been updated successfully."}
            )
        else:
            raise HTTPException(status_code=400, detail="Please provide a new email address.")
        
    else:
        raise HTTPException(status_code=400, detail="Invalid verification request.")
    
    db.commit()

    print(f"[VERIFY] email={verification.email} type={verification.token_type} used={verification.used}")

    secure = True if ENV == "PROD" else False
    samesite = "none" if ENV == "PROD" else "lax"
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=secure,
        samesite=samesite,
        path='/',
    )
    return response


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
        raise HTTPException(status_code=404, detail="Invalid credentials.")
    
    if user.is_verified: 
        raise HTTPException(status_code=409, detail="This email is already verified.")

    link = prepare_verification_link(db=db, email=payload.email, token_type="registration")
    send_mail_verification(purpose="NEW", reciever_mail_addr=payload.email, link=link)
    return JSONResponse(status_code=200, content= {"detail": "Verification email sent. Please check your inbox."})

