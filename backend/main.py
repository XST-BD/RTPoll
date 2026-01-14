import os
import sqlite3

from fastapi import FastAPI, Body
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Union

from db import cursor, conn
from service import send_mail_verification
from utils import validate_user_input, validate_db_entry

FRONTEND_URL1 = os.getenv('FRONTEND_URL1')
FRONTEND_URL2 = os.getenv('FRONTEND_URL2')

app = FastAPI()

origins = [
    FRONTEND_URL1,
    FRONTEND_URL2
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=str(origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/api/v0/user/register')
def register_user(
    username: str = Body(...),
    email: str = Body(...),
    password: str = Body(...)
):

    # Step 1: validate input
    error = validate_user_input(username, email, password)
    if error:
        raise HTTPException(status_code=400, detail=error)

    # Step 2: insert user into SQLite
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        # Handle unique constraint violations
        validate_db_entry(str(e).lower())

    send_mail_verification(email)
    return {"message": "Check your mail box to verify your account"}


# @app.post('/api/v0/user/login')
# def login_user(
    
# )