import asyncio
from contextlib import asynccontextmanager
from datetime import timezone, datetime

from fastapi import FastAPI, WebSocket

from app.db.model.poll import PollModel
from app.deps import SessionLocal
from app.services.history import sync_poll_history
from app.utils.poll import poll_timer

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    history_sync_task = asyncio.create_task(sync_poll_history())

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
    history_sync_task.cancel()
    await asyncio.gather(
        history_sync_task,
        return_exceptions=True
    )