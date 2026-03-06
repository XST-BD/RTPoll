import asyncio

from datetime import datetime, timezone

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.concurrency import run_in_threadpool

from jose import JWTError
import json
from pydantic import BaseModel
from sqlalchemy.orm import Session, selectinload

from app.db.model.poll import PollModel, PollOption
from app.db.model.user import UserModel
from app.deps import get_db, SessionLocal
from app.services.auth import decode_token
from app.setup.ws import wsmanager
from app.setup.cache import redis_client 

router = APIRouter()


class PollResponseModel(BaseModel):
    id: int
    question: str
    options: list[str]
    total_votes: int
    expires_at: datetime | str

    class Config:
        from_attributes = True

# service layer codes
    
def vote_percentages(
    votes: dict[int, int],
    option_count: int,
    poll_creator: bool
) -> list[int] | list[float]:

    total = sum(votes.values())

    if total == 0:
        if poll_creator:
            return [0] * option_count
        else:
            return [0.0] * option_count

    if poll_creator:
        return [
            round(votes.get(i, 0) / total * 100)
            for i in range(1, option_count + 1)
        ]
    else:
        return [
            round(votes.get(i, 0) / total * 100, 2)
            for i in range(1, option_count + 1)
        ]


@router.websocket('/vote/{poll_id}')
async def vote_ws(
    ws: WebSocket, 
    poll_id: int,
):
    await ws.accept()
    await wsmanager.connect(poll_id, ws)

    try: 
        # Send initial poll data (like /poll/view)
        db = SessionLocal()
        poll = db.query(PollModel).filter(PollModel.id==poll_id).first()

        if poll is None: 
            await ws.send_json({"type": "error", "message": "Poll not found"})
            return

        # Listen loop
        while True: 
            
            data = await ws.receive_json()
            msg_type = data.get("type")

            # ================================= VOTE ================================= #

            # Handle refresh 
            if msg_type == "send_vote":

                db = SessionLocal()

                try:
                    poll_vote = await run_in_threadpool(db.get, PollModel, poll_id)

                    if not poll_vote: 
                        await ws.send_json({"type": "error", "message": "Poll not found"})
                        continue
                
                    if poll_vote.expires_at and poll_vote.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc): 
                        await ws.send_json({"type": "error", "message": "This poll has ended"})
                        continue

                    try:
                        option_id = int(data.get("option_id"))
                    except (TypeError, ValueError):
                        await ws.send_json({"type": "error", "message": "Invalid option"})
                        continue
            
                    option = await run_in_threadpool(db.get, PollOption, option_id)
                    if not option or option.id != option_id:
                        await ws.send_json({"type": "error", "message": "Invalid option"})
                        continue

                    key = f'poll:{poll_id}:votes'

                    # Atomic increment
                    new_count = await redis_client.hincrby(key, str(option_id), 1) # type: ignore

                    # Broadcast update
                    await wsmanager.broadcast(
                        poll_id,
                        {
                            "type": "vote_update",
                            "option_id": option_id,
                            "count": new_count,
                        },
                    )
                finally: 
                    db.close()

            # Handle vote
            elif msg_type == "get_vote":
                db = SessionLocal()

                try: 
                    poll_vote = await run_in_threadpool(
                        lambda: db.query(PollModel)
                        .options(selectinload(PollModel.options))
                        .filter(PollModel.id == poll_id)
                        .first()
                    )

                    if poll_vote is None: 
                        await ws.send_json({"type": "error", "message": "Poll not found"})
                        continue
                
                    if poll_vote.expires_at and poll_vote.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc): 
                        await ws.send_json({"type": "notice", "message": "This poll has ended"})
                        continue
                    
                    # Read live votes from Redis
                    key = f'poll:{poll_id}:votes'
                    redis_votes = await redis_client.hgetall(key) # type: ignore
                    redis_votes = {int(k): int(v) for k, v in redis_votes.items()} # Convert to {option_id: count}
                    total_votes = sum(redis_votes.values())
                    votes_perc = vote_percentages(redis_votes, len(poll_vote.options), poll_vote.is_public)

                    votes_data = [
                        {
                            "id": opt.id,
                            "text": opt.text,
                            "votes_perc": votes_perc[i] if poll_vote.is_public else -1,
                        }
                        for i, opt in enumerate(poll_vote.options)
                    ]

                    expiry = "Never"
                    if poll_vote.expires_at: 
                       expiry = poll_vote.expires_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]+"Z"

                    
                    await ws.send_json({
                        "type": "vote_data", 
                        "question": poll_vote.question,
                        "options": votes_data,
                        "total_votes": total_votes  if poll_vote.is_public else -1,
                        "expiry": expiry,
                    })

                finally: 
                    db.close()

    except WebSocketDisconnect:
        wsmanager.disconnect(poll_id, ws)


@router.websocket("/poll/{poll_id}")
async def poll_ws(
    ws: WebSocket,
    poll_id: int,
    db: Session = Depends(get_db),
):
    await ws.accept()

    try:
        # ================= FIRST MESSAGE =================
        data = await ws.receive_json()

        token = data.get("token")
        msg_type = data.get("type")

        if not token:
            await ws.send_json({
                "type": "error",
                "message": "Missing access token"
            })
            await ws.close(code=1008)
            return

        # ================= AUTH =================
        try:
            payload = decode_token(token)
            email = payload.get("sub")

            user = (
                db.query(UserModel)
                .filter(UserModel.email == email)
                .first()
            )

            if not user:
                await ws.send_json({
                    "type": "error",
                    "message": "Unauthorized"
                })
                await ws.close(code=1008)
                return

        except JWTError:
            await ws.send_json({
                "type": "error",
                "message": "Invalid token"
            })
            await ws.close(code=1008)
            return

        # ================= CONNECT =================
        await wsmanager.connect(poll_id, ws)

        # ================= HANDLE FIRST REQUEST =================
        if msg_type == "poll_view":

            db = SessionLocal()

            try: 
                poll_vote = await run_in_threadpool(
                    lambda: db.query(PollModel)
                    .options(selectinload(PollModel.options))
                    .filter(PollModel.id == poll_id)
                    .first()
                )

                if poll_vote is None: 
                    await ws.send_json({"type": "error", "message": "Poll not found"})
                    return
                    
                # Read live votes from Redis
                key = f'poll:{poll_id}:votes'
                redis_votes = await redis_client.hgetall(key) # type: ignore
                redis_votes = {int(k): int(v) for k, v in redis_votes.items()} # Convert to {option_id: count}
                total_votes = sum(redis_votes.values())
                votes_perc = vote_percentages(redis_votes, len(poll_vote.options), poll_vote.is_public)

                votes_data = [
                    {
                        "id": opt.id,
                        "text": opt.text,
                        "votes": redis_votes.get(opt.id, 0),
                        "votes_perc": votes_perc[i],
                    }
                    for i, opt in enumerate(poll_vote.options)
                ]

                expiry = "Never"
                if poll_vote.expires_at: 
                   expiry = poll_vote.expires_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]+"Z"

                creation = poll_vote.created_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]+"Z"

                await ws.send_json({
                    "type": "poll_view", 
                    "result_public": poll_vote.is_public,
                    "question": poll_vote.question,
                    "options": votes_data,
                    "total_votes": total_votes,
                    "creation": creation,
                    "expiry": expiry,
                })

            finally:
                db.close()

        # ================= LISTEN LOOP =================
        while True:
            data = await ws.receive_json()
            msg_type = data.get("type")

            if msg_type == "poll_view":

                db = SessionLocal()

                try: 
                    poll_vote = await run_in_threadpool(
                        lambda: db.query(PollModel)
                        .options(selectinload(PollModel.options))
                        .filter(PollModel.id == poll_id)
                        .first()
                    )

                    if poll_vote is None: 
                        await ws.send_json({"type": "error", "message": "Poll not found"})
                        return
                    
                    # Read live votes from Redis
                    key = f'poll:{poll_id}:votes'
                    redis_votes = await redis_client.hgetall(key) # type: ignore
                    redis_votes = {int(k): int(v) for k, v in redis_votes.items()} # Convert to {option_id: count}
                    total_votes = sum(redis_votes.values())
                    votes_perc = vote_percentages(redis_votes, len(poll_vote.options), poll_vote.is_public)

                    votes_data = [
                        {
                            "id": opt.id,
                            "text": opt.text,
                            "votes": redis_votes.get(opt.id, 0),
                            "votes_perc": votes_perc[i]
                        }
                        for i, opt in enumerate(poll_vote.options)
                    ]

                    expiry = "Never"
                    if poll_vote.expires_at: 
                       expiry = poll_vote.expires_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]+"Z"

                    creation = poll_vote.created_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]+"Z"

                    await ws.send_json({
                        "type": "poll_view", 
                        "result_public": poll_vote.is_public,
                        "question": poll_vote.question,
                        "options": votes_data,
                        "total_votes": total_votes,
                        "creation": creation,
                        "expiry": expiry,
                    })
                
                finally: 
                    db.close()

    except WebSocketDisconnect:
        wsmanager.disconnect(poll_id, ws)



