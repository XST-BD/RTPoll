import sqlite3

from fastapi import FastAPI, Body, Depends
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session

from typing import Union

from app.db.base import Base, dbengine
from app.db.model.user import UserModel
from app.deps import get_db
from app.service import send_mail_verification, prepare_verification_link
from app.setup import app, cors_permit
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
        password=password,
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


# @app.post('/api/v0/user/login')
# def login_user(
    
# )