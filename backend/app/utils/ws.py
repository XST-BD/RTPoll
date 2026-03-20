from datetime import timezone
from typing import Any

from fastapi.concurrency import run_in_threadpool

from app.db.model.poll import PollModel
from app.deps import SessionLocal
from app.setup.cache import redis_client
from app.utils.vote import vote_percentages

async def create_payload(
        response_type: str, 
        key: str, 
        poll: PollModel
    ) -> Any:

    redis_votes = await redis_client.hgetall(key) # type: ignore
    redis_votes = {int(k): int(v) for k, v in redis_votes.items()} # Convert to {option_id: count}
    total_votes = sum(redis_votes.values())
    option_ids = [opt.id for opt in poll.options]
    votes_perc = vote_percentages(redis_votes, option_ids)

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
    
async def transform_for_creator(response_type: str, key: str, poll_id: int):

    db = SessionLocal()
    poll_vote = await run_in_threadpool(db.get, PollModel, poll_id)
    pass

async def transform_for_voter(response_type: str, key: str, poll_id: int):

    db = SessionLocal()
    poll_vote = await run_in_threadpool(db.get, PollModel, poll_id)
    pass
