from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from pydantic import BaseModel, Field
from sqlalchemy import or_
from sqlalchemy.orm import Session

from typing import List, Optional

from app.db.model.user import UserModel
from app.db.model.poll import PollModel
from app.deps import get_db
from app.service import get_current_user
from app.setup import CustomParams

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

    if is_indefinite: 
        return {
            "message": "Poll created",
            "id": poll.id,
            "is_indefinite": poll.is_indefinite,
            "expires_at": "never",
        }

    return {
        "message": "Poll created",
        "id": poll.id,
        "is_indefinite": poll.is_indefinite,
        "expires_at": poll.expires_at,
    }


class PollResponseModel(BaseModel):
    id: int
    question: str
    expires_at: Optional[datetime]
    is_indefinite: bool
    votes: int = 0
    top_pick: str = "Not implemented"

    class Config:
        from_attributes = True


@router.get('/poll/view', response_model=Page[PollResponseModel])
def poll_view(
    expired: bool = False,
    params: CustomParams = Depends(),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    
    now = datetime.now(timezone.utc)
    polls_query = db.query(PollModel).filter(PollModel.creator_id==user.user_id)

    if expired: 
        polls_query = polls_query.filter(
            PollModel.expires_at.isnot(None),
            PollModel.expires_at <= now
        )
                
    else: 
        polls_query = polls_query.filter(
            or_(
                PollModel.expires_at.is_(None),
                PollModel.expires_at > now
            )
        )

    polls_query = polls_query.order_by()
    return paginate(polls_query, params)


@router.get('/poll/result')
def poll_result(
    poll_id: str,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    poll = db.query(PollModel).filter(PollModel.id==poll_id)
    # TODO: Implement results
    return {"message": "poll result endpoint"}
