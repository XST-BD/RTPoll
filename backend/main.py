from app.api import auth, poll, user, vote, ws
from app.db.base import Base, dbengine
from app.setup import app, cors_permit, router

# must pre-load db models else model relationship will crash
from app.db.model.user import UserModel
from app.db.model.poll import PollModel

cors_permit()

Base.metadata.create_all(bind=dbengine)

@router.get('/')
async def response_root():
    return {"status": "ok"}

router.include_router(auth.router, prefix='/api/v0/auth', tags=['Authentication endpoint'])
router.include_router(poll.router, prefix='/api/v0/dashboard', tags=['Dashboard endpoint'])
router.include_router(user.router, prefix='/api/v0/user', tags=['User management endpoint'])
router.include_router(vote.router, prefix='/vote', tags=['Vote endpoint'])
router.include_router(ws.router, prefix='/ws', tags=['Websocket endpoint'])

app.include_router(router)



