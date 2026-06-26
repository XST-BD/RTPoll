from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, Request, BackgroundTasks, WebSocket
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from fastapi_pagination import paginate, Page
from pydantic import BaseModel, Field
from sqlalchemy import or_
from sqlalchemy.orm import Session

from typing import List, Optional

from app.db.model.user import UserModel
from app.db.model.poll import PollModel, PollOption, PollHistoryEntry
from app.deps import get_db
from app.services.auth import get_current_user
from app.setup.paginator import CustomParams
from app.setup.cache import redis_client
from app.setup.limiter import limiter
from app.setup.ws import wsmanager
from app.utils.poll import poll_timer

router = APIRouter()

class CreatePollRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1024)
    options: List[str] = Field(min_length=1, max_length=256)
    expires_at: Optional[datetime] = None
    result_public: bool = False


@router.post('', description="[FROZEN] Poll creation endpoint")
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
        bgtasks.add_task(poll_timer, poll.id, poll.expires_at) # type: ignore

    return {"poll_id": poll.id, "message": "Poll created successfully"}

class PollResponseModel(BaseModel):
    creator_id: str
    created_at: datetime | str
    question: str
    expires_at: datetime | str
    is_indefinite: bool
    total_votes: int
    options: list[tuple[str, str, int, float]]

    class Config:
        from_attributes = True


@router.get('/{poll_id}', response_model=PollResponseModel)
async def poll_view(
    poll_id: str,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    poll = db.query(PollModel).filter(PollModel.id==poll_id).first()

    if poll is None: 
        raise HTTPException(status_code=404, detail="Poll not found")
    
    # Redis live votes
    key = f'poll:{poll.id}:votes'
    redis_votes = await redis_client.hgetall(key)  # type: ignore
    redis_votes = {str(k): int(v) for k, v in redis_votes.items()}
    
    poll_expires_at = "Never" if poll.expires_at is None else poll.expires_at.replace(tzinfo=timezone.utc)
    total_votes = sum(redis_votes.values())

    poll_options = [
        (
            row.id, 
            row.text, 
            row.votes,
            round((row.votes / total_votes) * 100.00, 1) if total_votes else 0.00
        )
        for row in db.query(PollOption.id, PollOption.text, PollOption.votes).filter_by(poll_id=poll.id)
    ]

    respnose_data = PollResponseModel(
        creator_id=poll.creator_id,
        created_at=poll.created_at,
        question=poll.question,
        expires_at=poll_expires_at,
        is_indefinite=poll.is_indefinite,
        total_votes=total_votes,
        options=poll_options,
    )

    return respnose_data


@router.delete('/{poll_id}')
async def poll_delete(
    poll_id: str,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    poll = db.query(PollModel).filter(PollModel.id==poll_id).first()

    if poll is None: 
        raise HTTPException(status_code=404, detail="Poll not found")
    
    db.delete(poll)
    # Clean Redis cache of the poll
    await redis_client.delete(f'poll:{poll_id}:votes')
    # Broadcast poll deletion message
    await wsmanager.broadcast(
        poll_id=poll.id,
        payload={"type": "error", "message": "Poll not found or deleted"},
    )
    db.commit()
    
    return {"message": f"Poll: {poll_id} deleted successfully"}


class PollResponseAllModel(BaseModel):
    id: str
    question: str
    expires_at: datetime | str
    top_option: str
    total_votes: int

    class Config:
        from_attributes = True

@router.get('', response_model=Page[PollResponseAllModel], description="[FROZEN] Endpoint to get all associated poll of user")
@limiter.limit('60/Minute')
async def poll_view_all(
    request: Request,
    expired: bool = False,
    params: CustomParams = Depends(),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    
    if user is None: 
        raise HTTPException(status_code=404, detail="User not found")

    now = datetime.now(timezone.utc)
    polls_query = db.query(PollModel).filter(PollModel.creator_id==user.user_id)

    if polls_query is None:
        raise HTTPException(status_code=404, detail="Poll not found")

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
        redis_votes = {str(k): int(v) for k, v in redis_votes.items()}

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

@router.delete('')
async def poll_delete_all(
    expired: bool = False,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    polls = db.query(PollModel).filter(PollModel.creator_id==user.user_id)
    now = datetime.now(timezone.utc)
    ws = WebSocket

    if expired: 
        polls_query = polls.filter(
            PollModel.expires_at.isnot(None),
            PollModel.expires_at <= now
        )

        for poll in polls_query: 
            db.delete(poll)
            # Clean Redis for each poll
            await redis_client.delete(f'poll:{poll.id}:votes')
            # Broadcast poll deletion message
            await wsmanager.broadcast(
                poll_id=poll.id,
                payload={"type": "error", "message": "Poll not found or deleted"},
            )

    else:
        for poll in polls: 
            db.delete(poll)
            # Clean Redis for each poll
            await redis_client.delete(f'poll:{poll.id}:votes')
            # Broadcast poll deletion message
            await wsmanager.broadcast(
                poll_id=poll.id,
                payload={"type": "error", "message": "Poll not found or deleted"}
            )

    db.commit()

    return {"message": "All polls deleted"}


class PollGraphPoint(BaseModel):
    x: str
    y: int
class PollGraphResponseModel(BaseModel):
    poll_history_record: list[PollGraphPoint]

@router.get(
    "/{poll_id}/history",
    response_model=PollGraphResponseModel,
    description="Endpoint to get poll history graph data",
)
@limiter.limit("12/minute")
async def poll_get_history(
    request: Request,
    poll_id: str,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    poll_history = (
        db.query(PollHistoryEntry)
        .filter(PollHistoryEntry.poll_id == poll_id)
        .order_by(PollHistoryEntry.timestamp)
        .all()
    )

    if not poll_history:
        raise HTTPException(
            status_code=404,
            detail="Poll history not found",
        )

    first_record = poll_history[0]
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    poll_age = now - first_record.timestamp

    # Poll age <= 1 day -> single point
    if poll_age <= timedelta(days=1):
        latest = poll_history[-1]

        return PollGraphResponseModel(
            poll_history_record=[
                PollGraphPoint(
                    x=latest.timestamp.strftime("%Y-%m-%d"),
                    y=latest.value,
                )
            ]
        )

    # Poll age > 1 day -> latest value for each day
    daily_points: dict[str, int] = {}

    for history in poll_history:
        day = history.timestamp.strftime("%Y-%m-%d")
        daily_points[day] = history.value

    return PollGraphResponseModel(
        poll_history_record=[
            PollGraphPoint(x=day, y=value)
            for day, value in daily_points.items()
        ]
    )