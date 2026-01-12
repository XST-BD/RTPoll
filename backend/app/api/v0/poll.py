import datetime

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from sqlalchemy.orm import Session

from app.api.deps import get_db 
from app.api.v0.auth import get_current_user
from app.core.security import auth_scheme
from app.db.model.poll import PollModel 
from app.db.model.user import UserModel
from app.services.poll_service import generate_poll_slug, send_poll_email
from app.schemas.poll import PollCreate, PollView


router = APIRouter()

@router.post('/createpoll', dependencies=[Depends(auth_scheme)])
async def create_poll(
    poll: PollCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user) # JWT lock
):

    poll_slug = generate_poll_slug()
    poll_expires_at = datetime.datetime.now() + datetime.timedelta(poll.expires_at)

    new_poll = PollModel(
        question=poll.question, 
        options=poll.options,
        slug=poll_slug,
        creator_id=current_user.id,  # links poll to user
        creator_name=current_user.name,
        expires_at= poll_expires_at,
    )

    db.add(new_poll)
    db.commit()
    db.refresh(new_poll)

    # send email in background
    background_tasks.add_task(
        send_poll_email,
        to=current_user.email,
        poll_url=f"/{poll_slug}",
        expires_at=poll_expires_at,
    )

    return new_poll

@router.get('/getpoll/{poll_slug}', response_model= PollView)
async def view_poll(
    poll_slug: int, db: Session = Depends(get_db)
):
    poll = db.query(PollModel).filter(PollModel.slug == poll_slug).first()
    
    poll = (
        db.query(PollModel)
        .filter(
            PollModel.slug == poll_slug,
            PollModel.expires_at > datetime.datetime.now()
        )
        .first()
    )

    if not poll:
        raise HTTPException(status_code=404, detail="Poll expired or not found")

    return poll

@router.get('/getpoll_all', response_model= list[PollView])
async def view_all_poll(db: Session = Depends(get_db)):
    all_polls = db.query(PollModel).all()

    if not all_polls:
        raise HTTPException(status_code=404, detail="No poll created yet")

    return all_polls