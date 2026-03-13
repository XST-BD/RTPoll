from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.db.model.user import UserModel
from app.deps import hash_password, verify_password, get_db
from app.setup.vars import SECRET_KEY

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)


def decode_token(token: str):
    return jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])

# Protect routes
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = decode_token(token)
        email = payload.get("sub")
        db.expire_all()   # force fresh read from DB
        user = db.query(UserModel).filter(UserModel.email==email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
