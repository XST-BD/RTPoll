import asyncio
from contextlib import asynccontextmanager
from datetime import timezone, datetime

from fastapi import FastAPI

from app.db.model.poll import PollModel
from app.deps import SessionLocal
from app.setup.cache import sync_votes_db
from app.utils import poll_timer

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    sync_task = asyncio.create_task(sync_votes_db())

    # Start poll timers for unexpired polls
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        unexpired_polls = db.query(PollModel).filter(
            PollModel.expires_at != None,
            PollModel.expires_at > now
        ).all()
        for poll in unexpired_polls:
            if poll.expires_at:
                asyncio.create_task(poll_timer(poll.id, poll.expires_at))
    finally:
        db.close()
    
    yield  # FastAPI app is now running

    # --- Shutdown tasks ---
    sync_task.cancel()
    await asyncio.sleep(0)  # allow cancellation