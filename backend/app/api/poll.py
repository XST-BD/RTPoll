import asyncio
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks

from fastapi_pagination import paginate, Page
from pydantic import BaseModel, Field
from sqlalchemy import or_
from sqlalchemy.orm import Session

from typing import List, Optional

from app.db.model.user import UserModel
from app.db.model.poll import PollModel, PollHistoryEntry, PollOption
from app.deps import get_db
from app.services.auth import get_current_user
from app.services.history import sync_poll_history
from app.setup.paginator import CustomParams
from app.setup.limiter import limiter
from app.setup.cache import redis_client
from app.utils import poll_timer

router = APIRouter()


class CreatePollRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1024)
    options: List[str] = Field(min_length=1, max_length=256)
    expires_at: Optional[datetime] = None
    result_public: bool = False


@router.post('/poll')
async def poll_create(
    payload: CreatePollRequest, 
    bgtasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user)
):
    
    is_indefinite = payload.expires_at is None

    poll = PollModel(
        question=payload.question,
        creator_id=user.user_id,
        expires_at=payload.expires_at,
        is_indefinite=is_indefinite,
        is_public=payload.result_public,
        options=[
            PollOption(text=option_text, position=option_pos)
            for option_pos, option_text in enumerate(payload.options, start=1)
        ], 
    )

    db.add(poll)
    db.commit()
    db.refresh(poll)

    if poll.expires_at: 
        bgtasks.add_task(poll_timer, poll.id, poll.expires_at)

    return {
        "message": "Poll created",
        "id": poll.id,
        "is_indefinite": poll.is_indefinite,
        "expires_at": poll.expires_at if not is_indefinite else "never",
    }

class PollResponseModel(BaseModel):
    question: str
    expires_at: datetime | str
    total_votes: int

    class Config:
        from_attributes = True

@router.get('/poll/{poll_id}', response_model=PollResponseModel)
async def poll_view(
    poll_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    poll = db.query(PollModel).filter(PollModel.id==poll_id).first()

    if poll is None: 
        raise HTTPException(404, "Poll not found")
    
    # Redis live votes
    key = f'poll:{poll.id}:votes'
    redis_votes = await redis_client.hgetall(key)  # type: ignore
    redis_votes = {int(k): int(v) for k, v in redis_votes.items()}
    
    poll_expires_at = "Never" if poll.expires_at is None else poll.expires_at.replace(tzinfo=timezone.utc)
    total_votes = sum(redis_votes.values())

    PollResponseModel(
        question=poll.question,
        expires_at=poll_expires_at,
        total_votes=total_votes,
    )


@router.delete('/poll/{poll_id}')
async def poll_delete(
    poll_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    poll = db.query(PollModel).filter(PollModel.id==poll_id).first()

    if poll is None: 
        raise HTTPException(404, "Poll not found")
    
    db.delete(poll)
    db.commit()
    
    return {"message": f"Poll: {poll_id} deleted successfully"}



class PollResponseAllModel(BaseModel):
    id: int
    question: str
    expires_at: datetime | str
    top_option: str
    total_votes: int

    class Config:
        from_attributes = True


@router.get('/poll/all', response_model=Page[PollResponseAllModel])
async def poll_view_all(
    expired: bool = False,
    params: CustomParams = Depends(),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    
    if user is None: 
        raise HTTPException(404, "User not found")

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

        # Redis live votes
        key = f'poll:{poll.id}:votes'
        redis_votes = await redis_client.hgetall(key)  # type: ignore
        redis_votes = {int(k): int(v) for k, v in redis_votes.items()}

        if redis_votes: 
            top_option_id = max(redis_votes, key=lambda k: redis_votes[k])
            poll_top_pick = next(
                (opt.text for opt in poll.options if opt.id == top_option_id),
                "None"
            )
        else:
            poll_top_pick = "None"

        poll_expires_at = "Never" if poll.expires_at is None else poll.expires_at.replace(tzinfo=timezone.utc)

        total_votes = sum(redis_votes.values())

        items.append(
            PollResponseAllModel(
                id=poll.id,
                question=poll.question,
                expires_at=poll_expires_at,
                top_option=poll_top_pick,
                total_votes=total_votes,
            )
        )

    return paginate(items, params)

@router.delete('/poll/all')
async def poll_delete_all(
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    polls = db.query(PollModel).filter(PollModel.creator_id==user.id).all()

    for poll in polls: 
        db.delete(poll)

    db.commit()

    return {"message": "All polls deleted"}


# TODO: Add pagination
@router.get('/poll/result/{poll_id}')
@limiter.limit('5/Minute')  # Max 5 request per minute per IP
def poll_result(
    request: Request,
    poll_id: int,
    db: Session = Depends(get_db),
):
    
    entries = db.query(PollHistoryEntry)\
        .filter(PollHistoryEntry.poll_id == poll_id)\
        .order_by(PollHistoryEntry.timestamp).all()
    
    if not entries:
        return {"message": "Poll history is empty"}

    # To JSON format
    result = [{'x':  entry.timestamp.isoformat(), 'y': entry.value} for entry in entries]
    return result