from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request

from fastapi_pagination import paginate, Page
from pydantic import BaseModel, Field
from sqlalchemy import or_
from sqlalchemy.orm import Session

from typing import List, Optional

from app.db.model.user import UserModel
from app.db.model.poll import PollModel, PollHistoryEntry
from app.deps import get_db
from app.services.email import get_current_user
from app.setup.paginator import CustomParams
from app.setup.limiter import limiter

router = APIRouter()


class CreatePollRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1024)
    options: List[str] = Field(min_length=1, max_length=256)
    expires_at: Optional[datetime] = None
    result_public: bool = False


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


class PollResponseAllModel(BaseModel):
    id: int
    question: str
    expires_at: datetime | str

    class Config:
        from_attributes = True


@router.get('/poll/view/all', response_model=Page[PollResponseAllModel])
def poll_view(
    expired: bool = False,
    params: CustomParams = Depends(),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    
    now = datetime.now(timezone.utc)
    polls_query = db.query(PollModel).filter(PollModel.creator_id==user.user_id)

    if polls_query is None:
        raise HTTPException(404, "Poll not found")

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

    polls_query = polls_query.order_by(PollModel.created_at.desc())

    items = []

    for poll in polls_query: 

        poll_top_pick: str
        poll_expires_at: datetime | str
        # poll_total_votes: int = 0

        # for vote in poll.votes:
        #     poll_total_votes += 1

        if poll.votes:
            max_index = max(range(len(poll.votes)), key=lambda i: poll.votes[i])
            poll_top_pick = poll.options[max_index]
        else:
            poll_top_pick = "None"
        
        if poll.expires_at is None: 
            poll_expires_at = "Never"
        else:
            poll_expires_at = poll.expires_at

        items.append(
            PollResponseAllModel(
                id=poll.id,
                question=poll.question,
                expires_at=poll_expires_at,
            )
        )

    return paginate(items, params)

# TODO: Add pagination
@router.get('/poll/view/result/{poll_id}')
@limiter.limit('5/Minute')  # Max 5 request per minute per IP
def poll_result(
    request: Request,
    poll_id: int,
    db: Session = Depends(get_db),
):
    
    entries = db.query(PollHistoryEntry)\
        .filter(PollHistoryEntry.poll_id == poll_id)\
        .order_by(PollHistoryEntry.timestamp).all()
    
    if entries is None: 
        return {"message": "Poll history is empty or not found"}

    # To JSON format
    result = [{'x':  entry.timestamp.isoformat(), 'y': entry.value} for entry in entries]
    return result