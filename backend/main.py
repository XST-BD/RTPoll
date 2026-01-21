from fastapi import Depends

from app.api import auth, user
from app.db.base import Base, dbengine
from app.setup import app, cors_permit, router


cors_permit()

Base.metadata.create_all(bind=dbengine)

@router.get('/')
async def response_root():
    return {"status": "ok"}

router.include_router(auth.router, prefix='/v0/auth', tags=['Authentication endpoint'])
router.include_router(user.router, prefix='/v0/user', tags=['User management endpoint'])

app.include_router(router)


