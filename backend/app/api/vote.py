from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.db.model.poll import PollModel
from app.setup import redis_client
from app.service import wsmanager, get_db

router = APIRouter()

@router.post('/poll')
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