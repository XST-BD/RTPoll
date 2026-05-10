from datetime import datetime, timezone, timedelta
import uuid
from jose import jwt

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.utils.vote import create_token

router = APIRouter()


@router.post('/voter/token')
def visitor_token(request: Request):
    token = create_token()
    return JSONResponse(status_code=200, content={"token": token})