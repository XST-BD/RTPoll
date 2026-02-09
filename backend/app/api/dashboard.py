from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from pydantic import BaseModel, Field

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from typing import List, Optional

from app.db.model.user import UserModel
from app.db.model.poll import PollModel
from app.deps import get_db
from app.service import get_current_user

router = APIRouter()


class CreatePollRequest(BaseModel):
    question: str = Field(min_length=1, max_length=255)
    options: List[str] = Field()
    expires_at: Optional[datetime] = None


@router.post('/poll/create')
def poll_create(
    payload: CreatePollRequest, 
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user)
):
    
    is_indefinite = payload.expires_at is None

    poll = PollModel(
        question=payload.question,
        options=payload.options,
        creator_id=user.user_id,
        expires_at=payload.expires_at,
        is_indefinite=is_indefinite,
    )

    db.add(poll)
    db.commit()
    db.refresh(poll)

    return {
        "message": "Poll created",
        "id": poll.id,
        "is_indefinite": poll.is_indefinite,
        "expires_at": poll.expires_at,
    }


@router.get('/poll/view')
def poll_view(
    poll_id: int,
    db: Session = Depends(get_db)
):
    
    poll = db.query(PollModel).filter(PollModel.id==poll_id).first()
    
    if poll is None: 
        raise HTTPException(404, "Poll not found")
    
    if poll.expires_at is None:
        now = datetime.now(timezone.utc)

        if poll.expires_at is not None and poll.expires_at <= now:
            return {"message": "Requested poll already expired"}

    return poll

@router.get('/poll/result')
def poll_result(
    poll_id: str, 
    db: Session = Depends(get_db), 
    user: UserModel = Depends(get_current_user),
):
    poll = db.query(PollModel).filter(PollModel.id==poll_id)
    # TODO: Implement results
    return {"message": "poll result endpoint"}
