import hashlib

from fastapi import APIRouter, Request, Depends, Body, Cookie
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from typing import Optional

from sqlalchemy import select,func
from sqlalchemy.orm import Session

from app.db.model.user import UserModel, EmailVerification
from app.db.model.poll import PollModel
from app.deps import get_db, verify_password, hash_password, SessionLocal
from app.services.auth import create_access_token, decode_token, get_current_user
from app.services.email import send_mail_verification, prepare_verification_link
from app.setup.vars import router
from app.setup.limiter import limiter

router = APIRouter()

@router.post("/refresh", description="Refresh token endpoint")
async def refresh_token(
    refresh_token: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    
    try:
        payload = decode_token(refresh_token)
        email = payload.get("sub")
        user = db.query(UserModel).filter(UserModel.email==email).first()

        if user is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token({"sub": email})
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.get("/manage", description="Account details endpoint")
def view_account(
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    if not user.is_verified:
       raise HTTPException(400, "Unverified user")
    
    polls_created = db.query(PollModel).filter(PollModel.creator_id==user.user_id).count()

    with SessionLocal() as session:
        polls_expired =  session.scalar(
            select(func.count(PollModel.id))
                .where(
                    PollModel.creator_id == user.user_id,
                    PollModel.expires_at.is_not(None),
                    PollModel.expires_at < func.now()
                )
            )
    
    response = {
        "email": user.email, 
        "created_at": user.creation_date,
        "polls_created": polls_created,
        "polls_expired": polls_expired,
    }
    return response

@router.post("/manage", description="Email change endpoint")
def change_email(
    new_email: str = Body(...),
    old_email: str = Body(...),
    password: str = Body(...),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    if not user.is_verified:
       raise HTTPException(400, "Unverified user")
     
    if user.email != old_email: 
        raise HTTPException(400, "Wrong email")

    if not verify_password(password, user.password): 
        raise HTTPException(400, "Wrong password")
    
    user.email = new_email
    db.commit()
    db.refresh(user)

    response = {
        "message": "Email changed successfully",
        "new_email": user.email,
    }
    return response

@router.patch("/manage", description="Password recovery endpoint")
def recover_password(
    email: str = Body(...),
    db: Session = Depends(get_db),
):
    user = db.query(UserModel).filter(UserModel.email==email).first()

    if user is None: 
        raise HTTPException(400, "Unregistered user")
    
    if not user.is_verified:
        raise HTTPException(400, "Unverified user")
    
    link = prepare_verification_link(db=db, email=email)
    send_mail_verification(email, link)
    return {"message": "Mail verification sent"}
    
class ChangePasswordRequest(BaseModel):
    recovery: bool
    old_password: Optional[str]
    new_password: str

@router.put("/manage", description="Password change endpoint")
def change_password(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    if not user.is_verified:
        raise HTTPException(400, "Unverified user")
    
    if not payload.recovery and payload.old_password:
        if not verify_password(payload.old_password, user.password): 
            raise HTTPException(400, "Wrong old password")

    hashed_password = hash_password(payload.new_password)
    user.password = hashed_password
    db.commit()
    db.refresh(user)

    return {"message": "Password changed successfully"}

class DeleteAccRequest(BaseModel):
    password: str

@router.delete("/manage", description="Account deletion endpoint", status_code=204)
def delete_account(
    payload: DeleteAccRequest,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    if not user.is_verified:
        raise HTTPException(400, "Unverified user")

    if not verify_password(payload.password, user.password): 
        raise HTTPException(400, "Wrong password")
    
    db_user = db.query(UserModel).filter(UserModel.user_id == user.user_id).first()
    
    if db_user:
        db_user.is_active = False
        db_user.is_verified = False

        polls = db.query(PollModel).filter(PollModel.creator_id==db_user.user_id).all()

        for poll in polls: 
            db.delete(poll)

        db.commit()
        print(f"Active:", db_user.is_active)


class MailVerifyRequest(BaseModel):
    type: str
    token: str

@router.post("/verify", description="Mail verification endpoint")
def verify_mail(
    request: Request,
    payload: MailVerifyRequest, 
    db: Session = Depends(get_db),
):
    # token setup
    record = None
    if payload.type == "registration":
        token_hash = hashlib.sha256(payload.token.encode()).hexdigest()
        record = db.query(EmailVerification).filter(EmailVerification.token_hash==token_hash).first()
    else:
        return {"error": "Unknown type"}

    if not record:
        return {"error": "Invalid link"}
    
    if record.used: 
        return {"message": "Link is already used and expired"}
    
    user = (db.query(UserModel).filter(UserModel.email==record.email).first())
    if user is None:
        return {"error": "User not found"}

    user.is_verified = True
    record.used = True

    db.commit()

    return {"message": "User is verified"}


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

    if not user: 
        return {"error": "User not found during mail validation"}
    
    if user.is_verified: 
        return {"message": "User already verified"}

    link = prepare_verification_link(db=db, email=payload.email)
    send_mail_verification(payload.email, link)
    return {"message": "Mail verification sent"}


