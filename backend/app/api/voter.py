from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request 
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.db.model.user import UserModel
from app.db.model.poll import PollModel, PollOption
from app.deps import get_db
from app.services.auth import get_current_user
from app.setup.cache import redis_client

router = APIRouter()

class VoterResponseModel(BaseModel):
    question: str
    expires_at: datetime | str
    total_votes: int
    options: list[tuple[str, str, int, float]]
    class Config:
        from_attributes = True


@router.get('/{poll_id}', response_model=VoterResponseModel)
async def poll_view(
    poll_id: str,
    db: Session = Depends(get_db),
):
    poll = db.query(PollModel).filter(PollModel.id==poll_id).first()

    if poll is None: 
        return JSONResponse(content={"message": "Poll not found"}, status_code=404)

    if poll.expires_at and poll.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc): 
        return JSONResponse(content={"message": "This poll has expired"}, status_code=204)
    
    # Redis live votes
    key = f'poll:{poll.id}:votes'
    redis_votes = await redis_client.hgetall(key)  # type: ignore
    redis_votes = {str(k): int(v) for k, v in redis_votes.items()}
    
    poll_expires_at = "Never" if poll.expires_at is None else poll.expires_at.replace(tzinfo=timezone.utc)
    total_votes = sum(redis_votes.values())

    if poll.is_public :
        poll_options = [
            (
                row.id, 
                row.text, 
                row.votes,
                round((row.votes / total_votes) * 100.00, 1) if total_votes else 0.00
            )
            for row in db.query(PollOption.id, PollOption.text, PollOption.votes).filter_by(poll_id=poll.id)
        ]
    else: 
        poll_options = [
            (row.id, row.text, -1, -1.00)
            for row in db.query(PollOption.id, PollOption.text, PollOption.votes).filter_by(poll_id=poll.id)
        ]

    respnose_data = VoterResponseModel(
        question=poll.question,
        expires_at=poll_expires_at,
        total_votes=total_votes,
        options=poll_options,
    )

    return respnose_data
