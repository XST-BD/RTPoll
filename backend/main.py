import sqlite3

from fastapi import FastAPI, Body, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from typing import Union

from app.db.base import Base, dbengine
from app.db.model.user import UserModel
from app.deps import get_db, hash_password, verify_password
from app.service import send_mail_verification, prepare_verification_link
from app.setup import app, cors_permit, FRONTEND_URL1
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
    except sqlite3.IntegrityError as e:
        db.rollback()
        # Handle unique constraint violations
        validate_db_entry(str(e).lower())

    db.refresh(new_user)

    link = prepare_verification_link(username, db)
    send_mail_verification(email, link)
    return {"message": "Check your mail box to verify your account"}


@app.post('/api/v0/user/login')
def login_user(
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
    
    response = RedirectResponse(
        url=f"{FRONTEND_URL1}/dashboard",
        status_code=302
    )

    response.set_cookie(
        key='user_id', 
        value=user.user_id,
        httponly=True,
        secure=False,  # only in local dev
        samesite='lax',
        domain="localhost",
    )

    return response


@app.post('/api/v0/user/logout')
def logout_user(

):
    pass