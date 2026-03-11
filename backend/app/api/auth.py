import hashlib

from fastapi import APIRouter, Request, Depends, Body, Cookie
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse

from pydantic import BaseModel
from typing import Optional

from sqlalchemy.orm import Session

from app.db.model.user import UserModel, EmailVerification
from app.deps import get_db, verify_password, hash_password
from app.services.auth import create_access_token, decode_token, get_current_user
from app.services.email import send_mail_verification, prepare_verification_link
from app.setup.vars import router, FRONTEND_URL
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
    user: UserModel = Depends(get_current_user),
):
    if not user.is_verified:
       raise HTTPException(400, "Unverified user")
    
    response = {
        "user_id": user.user_id, 
        "email": user.email, 
        "created_at": user.creation_date,
        "polls_created": user.polls,
        "verified": user.is_verified,
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

    link = prepare_verification_link(db, email)
    send_mail_verification(email, link)


@router.put("/manage", description="Password change endpoint")
def change_password(
    old_password: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    if not user.is_verified:
        raise HTTPException(400, "Unverified user")
    
    if not verify_password(old_password, user.password): 
        raise HTTPException(400, "Wrong old password")

    hashed_password = hash_password(new_password)
    user.password = hashed_password
    db.commit()
    db.refresh(user)

    return {"message": "Password changed successfully"}


@router.delete("/manage", description="Account deletion endpoint")
def delete_account(
    password: str = Body(...),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    if not user.is_verified:
        raise HTTPException(400, "Unverified user")

    if not verify_password(password, user.password): 
        raise HTTPException(400, "Wrong password")
    
    db.delete(user)
    db.commit()

    return {"message": "Account deleted successfully"}


@router.post("/verify", description="Mail verification endpoint")
def verify_mail(
    request: Request,
    token: str, 
    recovery: bool,
    new_password: str = Body(...),
    db: Session = Depends(get_db),
):
    # Detect scanners 
    accept = request.headers.get("accept", "")

    # Block non-browser navigation
    if "text/html" not in accept: 
        return {"message": "verification link"}

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

    if not recovery:
        user.is_verified = True
        record.used = True
    else:
        user.password = hash_password(new_password)

    db.commit()

    return RedirectResponse(
        url=f"{FRONTEND_URL}/login",
        status_code=302
    )


class ResendMailRequest(BaseModel):
    email: str

@router.post("/resend", description="Mail resend endpoint")
@limiter.limit('5/minute')   # allow max 5 requests per minute per IP
def resend_mail(
    request: Request,
    payload: ResendMailRequest,
    db: Session = Depends(get_db),
):
    link = prepare_verification_link(db=db, email=payload.email)
    send_mail_verification(payload.email, link)
    return {"message": "Mail verification sent"}


