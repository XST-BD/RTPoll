from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse

from app.db.model.user import UserModel
from app.services.auth import get_current_user
from app.utils.vote import create_token


router = APIRouter()

@router.post('/visitor/token')
def visitor_token(request: Request):
    token = create_token("visitor")
    return JSONResponse(status_code=200, content={"token": token})

@router.post('/creator/token')
def creator_token(
    request: Request,
    user: UserModel = Depends(get_current_user),
):
    token = create_token("creator")
    return JSONResponse(status_code=200, content={"token": token})

