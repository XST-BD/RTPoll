from datetime import datetime

from fastapi import APIRouter, Depends

from pydantic import BaseModel, Field

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from typing import List

from app.db.model.user import UserModel
from app.db.model.poll import PollModel
from app.deps import get_db
from app.service import get_current_user

router = APIRouter()


class CreatePollRequest(BaseModel):
    question: str = Field(min_length=1, max_length=255)
    options: List[str] = Field()
    expires_at: datetime


@router.post('/poll/create')
def poll_create(
    payload: CreatePollRequest, 
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user)
):
    
    poll = PollModel(
        question=payload.question, 
        creator_id=user.user_id, 
        options=payload.options,
        expires_at=payload.expires_at,
    )

    db.add(poll)
    db.commit()
    db.refresh(poll)
    return {"message": "Poll created", "Poll": poll.id}



@router.get('/poll/view')
def poll_view(
    poll_id: str,
    db: Session = Depends(get_db)
):
    
    poll = db.query(PollModel).filter(PollModel.id==poll_id)
    return {"message": "Poll view", "Poll": poll}


@router.get('/poll/result')
def poll_result(
    poll_id: str, 
    db: Session = Depends(get_db), 
    user: UserModel = Depends(get_current_user),
):
    poll = db.query(PollModel).filter(PollModel.id==poll_id)
    # TODO: Implement results
    return {"message": "poll result endpoint"}
