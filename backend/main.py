import os
from dotenv import load_dotenv
import re
import sqlite3

from fastapi import FastAPI, Body
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Union

load_dotenv()
FRONTEND_URL1 = os.getenv('FRONTEND_URL1')
FRONTEND_URL2 = os.getenv('FRONTEND_URL2')
DATABASE_URL = os.getenv('DATABASE_URL')

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

conn = sqlite3.connect(str(DATABASE_URL), check_same_thread=False)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()

def validate_user_input(username: str, email: str, password: str):
    # Username: only letters, numbers, underscores
    if not re.fullmatch(r'\w+', username):
        return "Username can only contain letters, numbers, and underscores"
    
    if len(username) < 4:
        return "Username can't have less than 4 characters"

    # Email: simple regex check
    if not re.fullmatch(r'[^@]+@[^@]+\.[^@]+', email):
        return "Invalid email format"

    # Password: min len 8
    if len(password) < 8:
        return "Password must be at least 8 characters long"

    return None

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
        if "username" in str(e).lower():
            raise HTTPException(status_code=400, detail="Username already taken")
        elif "email" in str(e).lower():
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            raise HTTPException(status_code=400, detail="Database error")

    return {"message": "User registered successfully!"}