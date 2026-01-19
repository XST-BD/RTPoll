import secrets
import sqlite3

from fastapi import FastAPI, APIRouter, Body, Depends, Cookie, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse, JSONResponse

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from starlette.middleware.sessions import SessionMiddleware

from typing import Union

from app.db.base import Base, dbengine
from app.db.model.user import UserModel
from app.deps import get_db, hash_password, verify_password
from app.service import send_mail_verification, prepare_verification_link, get_current_user_state
from app.setup import app, cors_permit, FRONTEND_URL1, SECRET_KEY
from app.utils import validate_user_input, validate_db_entry


cors_permit()

Base.metadata.create_all(bind=dbengine)

@app.post('/api/v0/user/register')
def register_user(
    username: str = Body(...),
    email: str = Body(...),
    password: str = Body(...),
    db: Session = Depends(get_db)
):

    # Step 1: validate input
    error = validate_user_input(username, email, password)
    if error:
        raise HTTPException(status_code=400, detail=error)

    # Step 2: insert user into SQLite
    new_user = UserModel(
        username=username, 
        email=email,
        password=hash_password(password),
    )

    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError as e:
        db.rollback()
        # Handle db constraint violations
        validate_db_entry(str(e.orig).lower())


    link = prepare_verification_link(username, db)
    send_mail_verification(email, link)
    return {"message": "Check your mail box to verify your account"}


@app.post('/api/v0/user/login')
def login_user(
    request: Request,
    email: str = Body(...), 
    password: str = Body(...),
    db: Session = Depends(get_db)
):
    
    user = db.query(UserModel).filter(UserModel.email==email).first()

    if user is None: 
        raise HTTPException(status_code=400, detail="User not found")
    
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="User is not verified")
    
    if not verify_password(password, user.password): 
        raise HTTPException(status_code=400, detail="Wrong password")
    
    request.session['user_id'] = user.user_id

    return {"message": "Logged in successfully"}


@app.post('/api/v0/user/logout')
def logout_user(
    request: Request,
):
    # clear sessions
    request.session.clear()

    return {"message": "Logged out successfully"}


@app.get('/api/v0/auth/check')
def check_auth(
    user_id: str = Depends(get_current_user_state)
):

    if user_id is None: 
        raise HTTPException(status_code=401, detail="Not authenticated")

    return {
        "authenticated": True,
        "user_id": user_id,
    }