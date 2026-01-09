from fastapi import FastAPI, APIRouter

from app.api.v0 import poll
from app.db.base import Base, dbengine

app = FastAPI()
Base.metadata.create_all(bind=dbengine)

router = APIRouter(prefix='/api')

@router.get('/')
async def response_root():
    return {"status": "ok"}

router.include_router(poll.router, prefix='/v0', tags=['Poll creation and view']) 

app.include_router(router) 
