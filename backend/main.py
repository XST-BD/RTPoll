from app.api import auth, user, verify, poll, voter, token
from app.api.ws import polling
from app.db.base import Base, dbengine
from app.setup.vars import app, router
from app.setup.cors import cors_permit

# must pre-load db models else model relationship will crash
from app.db.model.user import UserModel
from app.db.model.poll import PollModel

cors_permit()

Base.metadata.create_all(bind=dbengine)

@router.get('/')
async def response_root():
    return {"status": "ok"}

router.include_router(auth.router, prefix='/api/v0/auth', tags=['Authentication endpoints'])
router.include_router(verify.router, prefix='/api/v0/auth/email', tags=['Mail verification endpoints'])
router.include_router(user.router, prefix='/api/v0/user', tags=['User state management endpoints'])
router.include_router(poll.router, prefix='/api/v0/poll', tags=['Poll state management endpoints'])
router.include_router(token.router, prefix='/api/v0/poll', tags=['Poll token management endpoints'])
router.include_router(voter.router, prefix='/api/v0/voter', tags=['Voter endpoints'])

router.include_router(polling.router, prefix='/api/v0/ws', tags=['Websocket endpoints for poll creator'])

app.include_router(router)




