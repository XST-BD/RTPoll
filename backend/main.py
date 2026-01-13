import os

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from dotenv import load_dotenv

# from app.api.v0 import poll, user, auth
from app.db.base import Base, dbengine

from app.api.v0 import user

load_dotenv()
FRONTEND_URL1 = os.getenv('FRONTEND_URL1')
FRONTEND_URL2 = os.getenv('FRONTEND_URL2')

app = FastAPI()
origins = [
    FRONTEND_URL1,
    FRONTEND_URL2
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=str(origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=dbengine)

router = APIRouter(prefix='/api')

@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc):
    err = exc.errors()[0]
    msg = str(err["msg"])
     # remove "ValueError: " if it exists
    if msg.startswith("ValueError: "):
        msg = msg[len("ValueError: "):]
    return JSONResponse(
        status_code=422,
        content={
            "field": err["loc"][-1],
            "message": err["msg"]
        }
    )


@router.get('/')
async def response_root():
    return {"status": "ok"}

# router.include_router(auth.router, prefix='/v0/auth', tags=['Authnetication endpoint'])
# router.include_router(poll.router, prefix='/v0', tags=['Poll creation and view']) 
router.include_router(user.router, prefix='/v0/user', tags=['User creation and view'])

app.include_router(router) 
