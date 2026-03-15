from fastapi import Depends, Body, APIRouter
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
from app.deps import hash_password

router = APIRouter()

@router.get("/", description="Account details endpoint")
def view_account(
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    if not user.is_verified:
       raise HTTPException(403, "Unverified user")
    
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
    return JSONResponse(status_code=200, content={"detail": response})


@router.post("/", description="Email change endpoint")
def change_email(
    new_email: str = Body(...),
    old_email: str = Body(...),
    password: str = Body(...),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    if not user.is_verified:
       raise HTTPException(403, "Unverified user")
     
    if user.email != old_email: 
        raise HTTPException(400, "Wrong email")

    if not verify_password(password, user.password): 
        raise HTTPException(400, "Wrong password")

    link = prepare_verification_link(db=db, email=new_email, token_type="email_change")
    send_mail_verification(new_email, link)
    
    return JSONResponse(status_code=200, content={"detail": "Check your mail box to verify your account"})


@router.put("/", description="Password change endpoint")
def change_password(
    old_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    if not user.is_verified:
        raise HTTPException(403, "Unverified user")
    
    if old_password:
        if not verify_password(old_password, user.password):
            raise HTTPException(400, "Wrong old password")

    hashed_password = hash_password(new_password)
    user.password = hashed_password
    db.commit()
    db.refresh(user)

    return JSONResponse(status_code=200, content={"detail": "Password changed successfully"})


@router.patch("/", description="Password recovery endpoint")
def recover_password(
    email: str = Body(...),
    db: Session = Depends(get_db),
):
    user = db.query(UserModel).filter(UserModel.email==email).first()

    if user is None: 
        raise HTTPException(403, "Unregistered user")
    
    if not user.is_verified:
        raise HTTPException(403, "Unverified user")
    
    link = prepare_verification_link(db=db, email=email, token_type="forgot_pass")
    send_mail_verification(email, link)
    return JSONResponse(status_code=200, content={"detail": "Mail verification sent"})


class DeleteAccRequest(BaseModel):
    password: str

@router.delete("/", description="Account deletion endpoint", status_code=204)
def delete_account(
    payload: DeleteAccRequest,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    if not user.is_verified:
        raise HTTPException(403, "Unverified user")

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
