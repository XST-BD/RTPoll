from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.model.poll import PollModel
from app.setup.cache import redis_client
from app.service import wsmanager, get_db

router = APIRouter()

@router.post('/poll/send')
async def recieve_vote(
    poll_id: int, 
    option_id: str,
    db: Session = Depends(get_db),
):
    
    # validate poll and option
    poll = db.query(PollModel).filter().first()

    if not poll:
        raise HTTPException(404, "Poll not found")
    
    if str(option_id) not in poll.options:
        raise HTTPException(400, "Invalid option")
    
    key = f'poll:{poll_id}:votes'

    # Atomic increment
    new_count = redis_client.hincrby(key, option_id, 1)

    await wsmanager.broadcast(
        poll_id,
        {"type": "update", "option_id": option_id, "count": new_count},
    )

    return {"status": "ok"}

class VoterPollResponseModel(BaseModel):
    question: str
    options: list[str]
    votes: list[int]

    class Config:
        from_attributes = True


@router.post('/poll/view', response_model=VoterPollResponseModel)
def voter_poll_view(
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
    

