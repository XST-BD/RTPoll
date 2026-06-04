import asyncio
from datetime import timezone, datetime

from fastapi import WebSocket
from fastapi.concurrency import run_in_threadpool

from sqlalchemy.orm import selectinload

from app.db.model.poll import PollModel
from app.deps import SessionLocal
from app.setup.ws import wsmanager

async def poll_timer(
    poll_id:str, expires_at: datetime
):
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

    await wsmanager.broadcast(
        poll_id=poll_id,
        payload={"type": "notice", "message": "This poll has ended"}
    )

def fetch_poll(poll_id: str):
    db = SessionLocal()
    try:
        poll = db.query(PollModel).options(selectinload(PollModel.options)).filter(PollModel.id == poll_id).first()
        return poll
    finally:
        db.close()


class WSConnectionManager:
    def __init__(self):
        self.creators: dict[str, WebSocket] = {}

    async def connect_creator(self, poll_id: str, ws: WebSocket):
        self.creators[poll_id] = ws

    async def send_to_creator(self, poll_id: str, data: dict):
        ws = self.creators.get(poll_id)
        if ws is None:
            return

        try:
            await ws.send_json(data)
        except Exception:
            self.creators.pop(poll_id, None)

    def disconnect_creator(self, poll_id: str):
        self.creators.pop(poll_id, None)

wsconnmanager = WSConnectionManager()