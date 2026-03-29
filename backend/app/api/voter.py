from datetime import datetime, timezone, timedelta
import uuid
from jose import jwt

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.setup.vars import SECRET_KEY

router = APIRouter()

ALGORITHM = "HS256"

@router.post('/voter/token')
def visitor_token(request: Request):
    
    auth = request.headers.get('Authorization')

    if auth:
        token = auth.split(' ')[1]
        try:
            jwt.decode(token, key=str(SECRET_KEY), algorithms=ALGORITHM)
            return JSONResponse(status_code=200, content={"token": token})
        except:
            pass

    # create new if token doesn't exist
    voter_id = str(uuid.uuid4())
    payload = {
        "vid": voter_id,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }
    token = jwt.encode(payload, key=str(SECRET_KEY), algorithm=ALGORITHM)

    return JSONResponse(status_code=200, content={"token": token})