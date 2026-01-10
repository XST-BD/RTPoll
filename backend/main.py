import os

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

from app.api.v0 import poll, user, auth
from app.db.base import Base, dbengine


load_dotenv()
FRONTEND_URL = os.getenv('FRONTEND_URL')

app = FastAPI()
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=dbengine)

router = APIRouter(prefix='/api')

@router.get('/')
async def response_root():
    return {"status": "ok"}

router.include_router(auth.router, prefix='/v0/auth', tags=['Authnetication endpoint'])
router.include_router(poll.router, prefix='/v0', tags=['Poll creation and view']) 
router.include_router(user.router, prefix='/v0/user', tags=['User creation and view'])

app.include_router(router) 
