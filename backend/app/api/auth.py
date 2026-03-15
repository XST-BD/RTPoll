from fastapi import APIRouter, Depends, Body, Cookie, Response
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.model.user import UserModel
from app.deps import get_db, verify_password, hash_password
from app.services.auth import create_access_token, decode_token, create_refresh_token
from app.services.email import send_mail_verification, prepare_verification_link
from app.setup.vars import ENV
from app.utils import validate_email


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
    return JSONResponse(status_code=200, content={"access_token": new_access_token, "token_type": "bearer"})


@router.post('/register')
def register_user(
    email: str = Body(...),
    password: str = Body(...),
    confirm_password: str = Body(...),
    db: Session = Depends(get_db),
):
    # Step 1: validate input
    if not validate_email(email):
        raise HTTPException(status_code=400, detail="Wrong mail format")

    # Step 2: check if email exists
    user = db.query(UserModel).filter(UserModel.email == email).first()

    if user:
        print(f"Active: ", user.is_active)
        if user.is_active:
            raise HTTPException(409, detail="Email already registered")
        
        # Password validation
        if len(password) < 8 or len(confirm_password) < 8:
            raise HTTPException(400, detail="Password must be 8 characters long")
        if password != confirm_password:
            raise HTTPException(status_code=400, detail="Passwords don't match")

        # Resurrection
        user.password = hash_password(password)
        user.is_active = True
        db.commit()

        link = prepare_verification_link(db=db, email=email, token_type="registration")
        send_mail_verification(email, link)
        
        return JSONResponse(status_code=200, content={"detail": "Check your mail box to verify your account"})
    
    
    # Password validation
    if len(password) < 8 or len(confirm_password) < 8:
        raise HTTPException(400, detail="Password must be 8 characters long")
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords don't match")

    # Step 4: insert user into SQLite
    new_user = UserModel(email=email, password=hash_password(password))
    new_user.is_verified = False
    new_user.is_active = True

    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError as e:
        db.rollback()
        db.expunge_all()  # remove all objects from session cache

    link = prepare_verification_link(db=db, email=email, token_type="registration")
    send_mail_verification(email, link)
    return JSONResponse(status_code=200, content={"detail": "Check your mail box to verify your account"})


@router.post('/login')
def login_user(
    email: str = Body(...), 
    password: str = Body(...),
    db: Session = Depends(get_db)
):
    
    user = db.query(UserModel).filter(UserModel.email==email).first()

    if user is None or not user.is_active: 
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="User is not verified")
    
    if not verify_password(password, user.password): 
        raise HTTPException(status_code=400, detail="Wrong password")
    
    access_token = create_access_token({'sub': email})
    refresh_token = create_refresh_token({'sub': email})
    response = JSONResponse(status_code=200, content={"access_token": access_token, "token_type": "bearer"})

    # Set refresh token in HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        max_age=7*24*60*60  # 7 days
    )
    return response


@router.post('/logout')
def logout_user(
    response: Response,
):
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=False,
        path='/',
    )
    
    return JSONResponse(status_code=200, content= {"detail": "Logged out successfully"})

