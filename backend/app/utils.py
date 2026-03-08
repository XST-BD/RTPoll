import re
from datetime import timezone
import dns.resolver
import dns.exception
from typing import Any

from fastapi.exceptions import HTTPException

from app.db.model.poll import PollModel
from app.setup.cache import redis_client

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


def validate_user_input(email: str, password: str):
    
    # Email: simple regex check
    if not validate_email(email):
        return "Invalid email format"

    # Password: min len 8
    if len(password) < 8:
        return "Password must be at least 8 characters long"

    return None


def validate_db_entry(err_msg: str):

    if "username" in err_msg:
            raise HTTPException(status_code=400, detail="Username already taken")
    elif "email" in err_msg:
        raise HTTPException(status_code=400, detail="Email already registered")
    elif "token" in err_msg:
            raise HTTPException(status_code=400, detail="Token already in use")
    else:
        raise HTTPException(status_code=400, detail="Database error")


def vote_percentages(
    votes: dict[int, int],
    option_ids: list[int],
    poll_creator: bool
) -> list[int] | list[float]:

    total = sum(votes.values())

    if total == 0:
        if poll_creator:
            return [0] * len(option_ids)
        else:
            return [0.0] * len(option_ids)

    if poll_creator:
        return [
            round(votes.get(opt_id, 0) / total * 100)
            for opt_id in option_ids
        ]
    else:
        return [
            round(votes.get(opt_id, 0) / total * 100, 2)
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