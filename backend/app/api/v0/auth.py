import os
import datetime
from dotenv import load_dotenv

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from jose import jwt

from app.api.deps import get_db
from app.core.security import verify_token_and_get_user, verify_password, auth_scheme
from app.db.model.user import UserModel

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(get_db)
):
    user = verify_token_and_get_user(token, db)

    if not user:
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Not authenticated",
       )

    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, key=str(SECRET_KEY), algorithm=ALGORITHM)


@router.post('/token')
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(UserModel).filter(
        UserModel.username == form_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }    
