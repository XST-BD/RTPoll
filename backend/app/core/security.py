from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from jose import jwt, JWTError
from datetime import datetime, timedelta

from app.db.model.user import UserModel

SECRET_KEY = "super-secret"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_minutes: int = 60):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token_and_get_user(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int | None = payload.get("sub")

        if user_id is None:
            return None
        
    except JWTError:
        return None 
    
    return db.query(UserModel).filter(UserModel.id == user_id).first()