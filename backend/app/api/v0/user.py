from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from pydantic import Field

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from app.api.deps import get_db, hash_password
from app.db.model.user import UserModel
from app.schemas.user import UserCreate, UserView
from app.utils.erorhandle import api_error

router = APIRouter()


@router.post('/register', response_model=UserView)
async def user_register(
    user: UserCreate, db: Session = Depends(get_db),
):
    
    new_user = UserModel(
        username=user.username, 
        email=user.email.lower().strip(),
        password=hash_password(user.password),
    )

    db.add(new_user)
    
    try:
        db.add(new_user)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        err_str = str(e.orig)

        if "uq_users_email" in err_str:
            return api_error("Email already registered", field="email", status_code=409)
        if "uq_users_username" in err_str:
            return api_error("Username already taken", field="username", status_code=409)

        return api_error("Invalid data", status_code=400)

    db.refresh(new_user)
    return new_user


# @router.get('/view/{username}', response_model=UserView)
# async def view_user(
#     username: str, db: Session = Depends(get_db)
# ):
#     user = db.query(UserModel).filter(UserModel.name == username).first()

#     if not user: 
#         raise HTTPException(status_code=404, detail="User not found")
    
#     return user


# @router.get('/viewall')
# async def view_user_all(
#     db: Session = Depends(get_db), response_model=list[UserView]
# ):
#     # TODO: implement admin object first

#     all_users = db.query(UserModel).all()

#     if not all_users:
#         raise HTTPException(status_code=404, detail="No user found :( ")

#     return all_users