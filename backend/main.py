from fastapi import Depends

from app.api import auth, dashboard, user
from app.db.base import Base, dbengine
from app.setup import app, cors_permit, router

from app.db.model.user import UserModel
from app.db.model.poll import PollModel

cors_permit()

Base.metadata.create_all(bind=dbengine)

@router.get('/')
async def response_root():
    return {"status": "ok"}

router.include_router(auth.router, prefix='/api/v0/auth', tags=['Authentication endpoint'])
router.include_router(dashboard.router, prefix='/api/v0/dashboard', tags=['Dashboard endpoint'])
router.include_router(user.router, prefix='/api/v0/user', tags=['User management endpoint'])

app.include_router(router)


