from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer 

from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import verify_token_and_get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    user = verify_token_and_get_user(token, db)

    if not user:
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Not authenticated",
       )

    return user