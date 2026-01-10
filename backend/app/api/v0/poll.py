from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db 
from app.api.v0.auth import get_current_user
from app.db.model.poll import PollModel 
from app.db.model.user import UserModel
from app.schemas.poll import PollCreate, PollView

router = APIRouter()

@router.post('/createpoll')
async def create_poll(
    poll: PollCreate, 
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user) # JWT lock
):

    new_poll = PollModel(
        question=poll.question, 
        options=poll.options,
        creator_id=current_user.id,  # links poll to user
        creator_name=current_user.name,
    )

    db.add(new_poll)
    db.commit()
    db.refresh(new_poll)

    return new_poll

@router.get('/getpoll/{poll_id}', response_model= PollView)
async def view_poll(
    poll_id: int, db: Session = Depends(get_db)
):
    poll = db.query(PollModel).filter(PollModel.id == poll_id).first()

    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")

    return poll

@router.get('/getpoll_all', response_model= list[PollView])
async def view_all_poll(db: Session = Depends(get_db)):
    all_polls = db.query(PollModel).all()

    if not all_polls:
        raise HTTPException(status_code=404, detail="No poll created yet")

    return all_polls