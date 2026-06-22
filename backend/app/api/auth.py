from fastapi import APIRouter, Depends, Body, Cookie, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.model.user import UserModel
from app.deps import get_db, verify_password, hash_password
from app.setup.limiter import limiter
from app.services.auth import create_access_token, decode_token, create_refresh_token
from app.services.email import send_mail_verification, prepare_verification_link
from app.setup.vars import ENV
from app.utils.email import validate_email


router = APIRouter()

@router.post("/refresh", description="[FROZEN] Refresh token endpoint")
@limiter.limit('10/Minute')
async def refresh_token(
    request: Request,
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


@router.post('/register', description="[FROZEN] User registration endpoint")
def register_user(
    email: str = Body(...),
    password: str = Body(...),
    confirm_password: str = Body(...),
    db: Session = Depends(get_db),
):
    # Step 1: validate input
    if not validate_email(email):
        raise HTTPException(status_code=400, detail="Please enter a valid email address.")

    # Password validation
    if len(password) < 8 or len(confirm_password) < 8:
        raise HTTPException(400, detail="Password must contain at least 8 characters.")
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    # Step 2: check if email exists
    user = db.query(UserModel).filter(UserModel.email == email).first()

    if user:
        print(f"Active: ", user.is_active)
        if user.is_active:
            raise HTTPException(409, detail="This email is already registered. Please login.")

        # Resurrection
        user.password = hash_password(password)
        user.is_active = True
        db.commit()

        link = prepare_verification_link(db=db, email=email, token_type="registration")
        send_mail_verification(purpose="NEW", reciever_mail_addr=email, link=link)
        
        return JSONResponse(status_code=201, content={"detail": "Verification email sent. Please check your inbox."})
    
    # Step 4: insert user into db
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
    send_mail_verification(purpose="NEW", reciever_mail_addr=email, link=link)
    return JSONResponse(status_code=200, content={"detail": "Verification email sent. Please check your inbox."})


@router.post('/login', description="[FROZEN] User login endpoint")
def login_user(
    email: str = Body(...), 
    password: str = Body(...),
    db: Session = Depends(get_db)
):
    
    user = db.query(UserModel).filter(UserModel.email==email).first()

    if user is None or not user.is_active: 
        raise HTTPException(status_code=404, detail="Invalid credentials.")
    
    if not verify_password(password, user.password): 
        raise HTTPException(status_code=400, detail="Invalid credentials.")
    
    if not user.is_verified:
        raise HTTPException(status_code=428, detail="Your email address is not verified yet. Please verify your email before logging in.")
    
    access_token = create_access_token({'sub': email})
    refresh_token = create_refresh_token({'sub': email})
    response = JSONResponse(status_code=200, content={"access_token": access_token, "token_type": "bearer"})

    secure = True if ENV == "PROD" else False
    samesite = "none" if ENV == "PROD" else "lax"

    # Set refresh token in HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=secure,
        samesite=samesite,
        max_age=7*24*60*60,  # 7 days
    )
    return response


@router.post('/logout', description="[FROZEN] User logout endpoint")
def logout_user():

    secure = True if ENV == "PROD" else False
    samesite = "none" if ENV == "PROD" else "lax"

    response = JSONResponse(
        status_code=200,
        content={"detail": "Logged out successfully."}
    )
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=secure,
        samesite=samesite,
        path='/',
    )
    
    return response

