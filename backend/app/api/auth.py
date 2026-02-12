import hashlib

from fastapi import APIRouter, Request, Depends, Body
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse

from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.db.model.user import UserModel, EmailVerification
from app.deps import get_db, verify_password, hash_password
from app.service import get_current_user_state, send_mail_verification, prepare_verification_link
from app.setup.vars import router, FRONTEND_URL
from app.setup.limiter import limiter

router = APIRouter()

@router.get('/check')
def check_auth(
    user_id: str = Depends(get_current_user_state)
):

    return {
        "authenticated": user_id is not None,
        "user_id": user_id,
    }

@router.patch('/recovery')
def recover_password(
    email: str = Body(...),
    password1: str = Body(...),
    password2: str = Body(...),
    db: Session = Depends(get_db),
):
    user = db.query(UserModel).filter(UserModel.email==email).first()

    if user is None: 
        raise HTTPException(400, "Unregistered user")
    
    if not user.is_verified:
        raise HTTPException(400, "Unverified user")
    
    if not verify_password(password1, password2): 
        raise HTTPException(400, "Passwords don't match")
    
    hashed_password = hash_password(password1)
    user.password = hashed_password
    db.commit()
    db.refresh(user)

    return {"message": "Password changed successfully"}
    

@router.get('/verify_mail')
def verify_mail(
    token: str, db: Session = Depends(get_db)
):
    # token setup
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    record = db.query(EmailVerification).filter(EmailVerification.token_hash==token_hash).first()

    if not record:
        raise HTTPException(status_code=400, detail="Invalid link")
    
    if record.used: 
        raise HTTPException(status_code=400, detail="Link is already used and expired")
    
    user = (db.query(UserModel).filter(UserModel.email==record.email).first())
    if user is None:
        raise HTTPException(status_code=400, detail="User not found during mail validation")

    user.is_verified = True
    record.used = True

    db.commit()

    return RedirectResponse(
        url=f"{FRONTEND_URL}/login",
        status_code=302
    )


class ResendMailRequest(BaseModel):
    email: str

@router.post('/resend_mail')
@limiter.limit('5/minute')   # allow max 5 requests per minute per IP
def resend_mail(
    request: Request,
    payload: ResendMailRequest,
    db: Session = Depends(get_db),
):
    link = prepare_verification_link(db=db, email=payload.email)
    send_mail_verification(payload.email, link)
    return {"message": "Mail verification sent"}


