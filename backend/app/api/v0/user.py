from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.deps import get_db, hash_password
from app.db.model.user import UserModel
from app.schemas.user import UserCreate, UserView

router = APIRouter()

@router.post('/create', response_model=UserView)
async def create_user(
    user: UserCreate, db: Session = Depends(get_db),
):
    
    new_user = UserModel(
        name=user.name, 
        email=user.email,
        password=hash_password(user.password),
        fingerprint=user.fingerprint,
    )

    db.add(new_user)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "users.email" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Email already registered"
            )
        raise HTTPException(status_code=400, detail="Invalid data")

    db.refresh(new_user)
    return new_user


@router.get('/view/{username}', response_model=UserView)
async def view_user(
    username: str, db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(UserModel.name == username).first()

    if not user: 
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.get('/viewall')
async def view_user_all(
    db: Session = Depends(get_db), response_model=list[UserView]
):
    # TODO: implement admin object first

    all_users = db.query(UserModel).all()

    if not all_users:
        raise HTTPException(status_code=404, detail="No user found :( ")

    return all_users