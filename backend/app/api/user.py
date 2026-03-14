from fastapi import APIRouter, Request, Body, Depends, Response
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse


from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.model.user import UserModel
from app.deps import get_db, hash_password, verify_password, SessionLocal
from app.services.auth import create_access_token, create_refresh_token, oauth2_scheme
from app.services.email import send_mail_verification, prepare_verification_link
from app.setup.vars import router
from app.utils import validate_user_input
from app.utils import validate_user_input


router = APIRouter()

@router.post('/register')
def register_user(
    email: str = Body(...),
    password: str = Body(...),
    db: Session = Depends(get_db),
):
    # Step 1: validate input
    error = validate_user_input(email, password)
    if error:
        raise HTTPException(status_code=400, detail=error)

    # Step 2: check if email exists
    user = db.query(UserModel).filter(UserModel.email == email).first()

    if user:
        print(f"Active: ", user.is_active)
        if user.is_active:
            raise HTTPException(400, "Email already registered")
        
        # Resurrection
        user.is_active = True
        user.password = hash_password(password)
        db.commit()
        link = prepare_verification_link(db=db, email=email)
        send_mail_verification(email, link)
        return {"message": "Check your mail box to verify your account"}

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

    link = prepare_verification_link(db=db, email=email)
    send_mail_verification(email, link)
    return {"message": "Check your mail box to verify your account"}


@router.post('/login')
def login_user(
    request: Request,
    email: str = Body(...), 
    password: str = Body(...),
    db: Session = Depends(get_db)
):
    
    user = db.query(UserModel).filter(UserModel.email==email).first()

    if user is None or not user.is_active: 
        raise HTTPException(status_code=400, detail="User not found")
    
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="User is not verified")
    
    if not verify_password(password, user.password): 
        raise HTTPException(status_code=400, detail="Wrong password")
    
    access_token = create_access_token({'sub': email})
    refresh_token = create_refresh_token({'sub': email})


    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    # Set refresh token in HttpOnly cookie
    # response.set_cookie(
    #     key="refresh_token",
    #     value=refresh_token,
    #     httponly=True,
    #     secure=False,
    #     samesite="lax",
    #     max_age=7*24*60*60  # 7 days
    # )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,       # must be True for HTTPS cross-origin
        samesite="none",   # allow cross-origin
        max_age=7*24*60*60
    )

    return response


@router.post('/logout')
def logout_user(
    response: Response,
):
    # response.delete_cookie(
    #     key="refresh_token",
    #     httponly=True,
    #     secure=False,
    #     samesite="lax",
    #     path='/',
    # )
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=True,
        samesite="none",
        path='/',
    )
    return {"message": "Logged out successfully"}

