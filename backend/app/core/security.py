import os
from dotenv import load_dotenv

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from jose import jwt, JWTError
from datetime import datetime, timedelta

from passlib.context import CryptContext

from app.api.deps import get_db

auth_scheme = HTTPBearer()
pwd_context = CryptContext(
    schemes=["bcrypt", "argon2"],
    deprecated="auto"
)

from app.db.model.user import UserModel

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_minutes: int = 60):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)

def verify_token_and_get_user(
        creds: HTTPAuthorizationCredentials = Depends(auth_scheme),
        db: Session = Depends(get_db)
    ):
    try:
        token = creds.credentials
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        user_id: int | None = payload.get("sub")

        if user_id is None:
            return None
        
    except JWTError:
        return None 
    
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def verify_password(plain_pwd: str, hashed_pwd: str) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)