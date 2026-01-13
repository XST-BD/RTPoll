import re

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from typing import Union

app = FastAPI()

def validate_user_input(username: str, email: str, password: str):
    # Username: only letters, numbers, underscores
    if not re.fullmatch(r'\w+', username):
        return "Username can only contain letters, numbers, and underscores."

    # Email: simple regex check
    if not re.fullmatch(r'[^@]+@[^@]+\.[^@]+', email):
        return "Invalid email format."

    # Password: at least 8 chars
    if len(password) < 8:
        return "Password must be at least 8 characters long."

    # All good
    return None

@app.post('/api/v0/user/register')
def register_user(username: str, email: str, password: str):

    error = validate_user_input(username, email, password)
    if error:
        raise HTTPException(status_code=400, detail=error)

    # TODO: add user creation here
    return {"message": "User registered successfully!"}