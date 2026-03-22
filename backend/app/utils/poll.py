import asyncio
from datetime import timezone, datetime

from fastapi.concurrency import run_in_threadpool

from sqlalchemy.orm import selectinload

from app.db.model.poll import PollModel
from app.deps import SessionLocal
from app.setup.ws import wsmanager
from app.utils.ws import create_payload

async def poll_timer(poll_id:str, expires_at: datetime):
    now = datetime.now(timezone.utc)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    remaining = (expires_at - now).total_seconds()
    if remaining > 0:
        await asyncio.sleep(remaining)

    # Broadcast to all connected clients (only show message, not counts if not public)
    db = SessionLocal()
    key = f'poll:{poll_id}:votes'
    poll_vote = await run_in_threadpool(db.get, PollModel, poll_id)
    creator_payload = await create_payload("poll_view", key, poll_vote)

    await wsmanager.broadcast(
        poll_id,
        voter_payload={"type": "notice", "message": "This poll has ended"},
        creator_payload= creator_payload,
    )

def fetch_poll(poll_id: str):
    db = SessionLocal()
    try:
        poll = db.query(PollModel).options(selectinload(PollModel.options)).filter(PollModel.id == poll_id).first()
        return poll
    finally:
        db.close()
