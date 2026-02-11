from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.model.poll import PollModel
from app.deps import get_db
from app.setup.cache import redis_client
from app.setup.ws import wsmanager

router = APIRouter()

class VoterPollResponseModel(BaseModel):
    question: str
    options: list[str]
    votes: list[int]

    class Config:
        from_attributes = True

# Fallback endpoint

@router.post('/poll/view', response_model=VoterPollResponseModel)
async def voter_poll_view(
    poll_id: int,
    db: Session = Depends(get_db),
):
    now = datetime.now(timezone.utc)
    poll = db.query(PollModel).filter(PollModel.id==poll_id).first()

    if poll is None: 
        raise HTTPException(404, "Poll not found")
    
    return VoterPollResponseModel(
        question=poll.question,
        options=poll.options,
        votes=poll.votes,
    )
    

