from datetime import date

from fastapi import Depends, Body, APIRouter, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from sqlalchemy import select,func
from sqlalchemy.orm import Session

from app.db.model.user import UserModel
from app.db.model.poll import PollModel
from app.deps import get_db, verify_password, hash_password, SessionLocal
from app.services.auth import get_current_user
from app.services.email import prepare_verification_link, send_mail_verification
from app.setup.limiter import limiter
from app.deps import hash_password

router = APIRouter()


class UserStatsResponse(BaseModel):
    email: str
    created_at: date
    total_polls: int
    expired_polls: int
    running_polls: int

@router.get("", description="[FROZEN] Account details endpoint", response_model=UserStatsResponse)
@limiter.limit('25/Minute')
def view_account(
    request: Request,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):    
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
    
    response = UserStatsResponse(
        email=user.email,
        created_at=user.creation_date,
        total_polls=polls_created,
        expired_polls=polls_expired if polls_expired else 0,
        running_polls= (polls_created - (polls_expired if polls_expired else 0)),
    )
    return response 


class ChangeEmailSchema(BaseModel):
    new_email: str
    password: str

@router.post("", description="Email change endpoint")
def change_email(
    payload: ChangeEmailSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    if not user.is_verified:
       raise HTTPException(403, "Unverified user")

    if not verify_password(payload.password, user.password): 
        raise HTTPException(400, "Wrong password")

    link = prepare_verification_link(db=db, email=payload.new_email, token_type="email_change", extra=user.email)
    send_mail_verification(payload.new_email, link)
    
    return JSONResponse(status_code=202, content={"detail": "Verification email sent. Please check your inbox."})


class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str

@router.put("", description="[FROZEN] Password change endpoint")
def change_password(
    payload: ChangePasswordSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):    
    if len(payload.new_password) < 8:
        raise HTTPException(status_code=406, detail="Password must contain at least 8 characters.")

    if payload.old_password:
        if not verify_password(payload.old_password, user.password):
            raise HTTPException(400, "Incorrect old password.")

    hashed_password = hash_password(payload.new_password)
    user.password = hashed_password
    db.commit()
    db.refresh(user)

    return JSONResponse(status_code=200, content={"detail": "Password updated successfully."})


class ForgotPasswordSchema(BaseModel):
    email: str

@router.patch("", description="Password recovery endpoint")
def recover_password(
    payload: ForgotPasswordSchema,
    db: Session = Depends(get_db),
):
    user = db.query(UserModel).filter(UserModel.email==payload.email).first()

    if user is None or not user.is_active: 
        raise HTTPException(404, "Invalid credentials.")
    
    if not user.is_verified:
        raise HTTPException(403, "Your email address is not verified yet. Please verify your email first.")
    
    link = prepare_verification_link(db, payload.email, token_type="forgot_pass")
    send_mail_verification(payload.email, link)
    return JSONResponse(status_code=202, content={"detail": "Password reset email sent successfully. Please check your inbox."})


class DeleteAccRequest(BaseModel):
    password: str

@router.delete("", description="[FROZEN] Account deletion endpoint", status_code=204)
def delete_account(
    payload: DeleteAccRequest,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    if not verify_password(payload.password, user.password): 
        raise HTTPException(
            status_code=400, detail="Incorrect password."
        )
    
    db_user = db.query(UserModel).filter(UserModel.user_id == user.user_id).first()
    
    if db_user:
        db_user.is_active = False
        db_user.is_verified = False

        polls = db.query(PollModel).filter(PollModel.creator_id==db_user.user_id).all()

        for poll in polls: 
            db.delete(poll)

        db.commit()
        print(f"Active:", db_user.is_active)
