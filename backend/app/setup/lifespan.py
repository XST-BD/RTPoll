import asyncio
from contextlib import asynccontextmanager
from datetime import timezone, datetime

from fastapi import FastAPI

from app.db.model.poll import PollModel
from app.deps import SessionLocal
from app.utils.poll import poll_timer

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Start poll timers for unexpired polls
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        unexpired_polls = (
            db.query(PollModel)
            .filter(
                PollModel.expires_at != None,
                PollModel.expires_at > now
            ).all()
        )

        for poll in unexpired_polls:
            if poll.expires_at:
                asyncio.create_task(poll_timer(poll_id=poll.id, expires_at=poll.expires_at))
    finally:
        db.close()
    
    yield  # FastAPI app is now running

    # Shutdown
    await asyncio.gather(return_exceptions=True)