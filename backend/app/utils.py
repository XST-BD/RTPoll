import asyncio
import re
from datetime import timezone, datetime
import dns.resolver
import dns.exception
from typing import Any

from fastapi.concurrency import run_in_threadpool
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import selectinload

from app.db.model.poll import PollModel
from app.deps import SessionLocal
from app.setup.cache import redis_client
from app.setup.ws import wsmanager

def validate_email(email_addr: str):
    # Step 1: Basic format check
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email_addr):
        return False

    # Step 2: Check if domain has MX record
    domain = email_addr.split("@")[1]
    try:
        answers = dns.resolver.resolve(domain, "MX")
        return len(answers) > 0
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout):
        return False

def vote_percentages(
    votes: dict[int, int],
    option_ids: list[int],
    poll_creator: bool
) -> list[float]:

    total = sum(votes.values())

    if total == 0:
        if poll_creator:
            return [0.0] * len(option_ids)
        else:
            return [0.0] * len(option_ids)

    if poll_creator:
        return [
            round(votes.get(opt_id, 0) / total * 100)
            for opt_id in option_ids
        ]
    else:
        return [
            round(votes.get(opt_id, 0) / total * 100)
            for opt_id in option_ids
        ]

async def create_payload(
        response_type: str, 
        key: str, 
        poll: PollModel
    ) -> Any:

    redis_votes = await redis_client.hgetall(key) # type: ignore
    redis_votes = {int(k): int(v) for k, v in redis_votes.items()} # Convert to {option_id: count}
    total_votes = sum(redis_votes.values())
    option_ids = [opt.id for opt in poll.options]
    votes_perc = vote_percentages(redis_votes, option_ids, poll.is_public)

    creator_votes_data = [
        {
            "id": opt.id,
            "text": opt.text,
            "votes": redis_votes.get(opt.id, 0),
            "votes_perc": votes_perc[i],
        }
        for i, opt in enumerate(poll.options)
    ]

    voter_votes_data = [
        {
            "id": opt.id,
            "text": opt.text,
            "votes_perc": votes_perc[i] if poll.is_public else -1,
        }
        for i, opt in enumerate(poll.options)
    ]

    expiry = "Never"
    if poll.expires_at: 
       expiry = poll.expires_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]+"Z"

    creation = poll.created_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]+"Z"

    if response_type == "poll_view":
        return {
            "type": response_type, 
            "result_public": poll.is_public,
            "question": poll.question,
            "options": creator_votes_data,
            "total_votes": total_votes,
            "creation": creation,
            "expiry": expiry,
        }
    elif response_type == "vote_data":
        return {
            "type": "vote_data", 
            "question": poll.question,
            "options": voter_votes_data,
            "total_votes": total_votes  if poll.is_public else -1,
            "expiry": expiry,
        }
    
async def poll_timer(poll_id:int, expires_at: datetime):
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
    creator_payload = create_payload("poll_view", key, poll_vote)

    await wsmanager.broadcast(
        poll_id,
        voter_payload={"type": "notice", "message": "This poll has ended"},
        creator_payload= creator_payload,
    )

def fetch_poll(poll_id: int):
    db = SessionLocal()
    try:
        poll = db.query(PollModel).options(selectinload(PollModel.options)).filter(PollModel.id == poll_id).first()
        return poll
    finally:
        db.close()