import asyncio

from datetime import datetime, timezone

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException

from jose import JWTError
import json
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.model.poll import PollModel
from app.db.model.user import UserModel
from app.deps import get_db, session_local
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

def vote_percentages(votes: list[int], poll_creator: bool) -> list[int] | list[float]:
    total = sum(votes)

    if poll_creator: 
        if total == 0:
            return [0] * len(votes)

        return [round(v / total * 100) for v in votes]
    else: 
        if total == 0:
            return [0.0] * len(votes)

        return [round(v / total * 100, 2) for v in votes]


@router.websocket('/vote/{poll_id}')
async def vote_ws(
    ws: WebSocket, 
    poll_id: int,
    db: Session = Depends(get_db),
):
    await ws.accept()
    await wsmanager.connect(poll_id, ws)

    try: 
        # Send initial poll data (like /poll/view)
        poll = db.query(PollModel).filter(PollModel.id==poll_id).first()

        if poll is None: 
            await ws.send_json({
                "type": "error", 
                "message": "Poll not found",
            })
            return

        # Listen loop
        while True: 
            
            lock = await redis_client.set("poll_sync_lock", "1", nx=True, ex=25)

            if not lock: 
                await asyncio.sleep(5)
                continue

            data = await ws.receive_json()
            msg_type = data.get("type")

            # ================================= VOTE ================================= #

            # Handle refresh 
            if msg_type == "send_vote":

                db = session_local
                poll_vote = db.get(PollModel, poll_id)

                if poll_vote is None: 
                    await ws.send_json({
                        "type": "error", 
                        "message": "Poll not found",
                    })
                    return
                
                if poll_vote.expires_at is not None: 
                    if poll_vote.expires_at < datetime.now(): 
                        await ws.send_json({
                            "type": "error", 
                            "message": "Polling ended",
                        })
                        return

                option_id: str = data.get("option_id")
                if option_id not in poll_vote.options:

                    await ws.send_json({
                        "type": "error",
                        "message": "Invalid option",
                    })
                    continue

                key = f'poll:{poll_id}:votes'

                # Atomic increment
                new_count = await redis_client.hincrby(key, option_id, 1) # type: ignore

                # Broadcast update
                await wsmanager.broadcast(
                    poll_id,
                    {
                        "type": "vote_update",
                        "option_id": option_id,
                        "count": new_count,
                    },
                )

            # Handle vote
            elif msg_type == "get_vote":
                db = session_local
                poll_vote = db.get(PollModel, poll_id)

                if poll_vote is None: 
                    await ws.send_json({
                        "type": "error", 
                        "message": "Poll not found",
                    })
                    return
                
                expiry = "Never"
                if poll_vote.expires_at: 
                   expiry = poll_vote.expires_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]+"Z"

                votes = vote_percentages(poll_vote.votes, False) if poll_vote.is_public else []

                await ws.send_json({
                    "type": "vote_data", 
                    "question": poll_vote.question,
                    "options": poll_vote.options,
                    "votes": votes,
                    "expiry": expiry,
                })

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

            db = session_local
            poll_vote = db.get(PollModel, poll_id)

            if poll_vote is None: 
                await ws.send_json({
                    "type": "error", 
                    "message": "Poll not found",
                })
                return
            
            votes_percantage = vote_percentages(poll_vote.votes, True)

            expiry = "Never"
            if poll_vote.expires_at: 
               expiry = poll_vote.expires_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]+"Z"

            creation = poll_vote.created_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]+"Z"

            await ws.send_json({
                "type": "poll_view", 
                "result_public": poll_vote.is_public,
                "question": poll_vote.question,
                "options": poll_vote.options,
                "votes": poll_vote.votes,
                "percantage": votes_percantage,
                "total_votes": sum(poll_vote.votes),
                "creation": creation,
                "expiry": expiry,
            })

        # ================= LISTEN LOOP =================
        while True:
            data = await ws.receive_json()
            msg_type = data.get("type")

            if msg_type == "poll_view":

                db = session_local
                poll_vote = db.get(PollModel, poll_id)

                if poll_vote is None: 
                    await ws.send_json({
                        "type": "error", 
                        "message": "Poll not found",
                    })
                    return

                votes_percantage = vote_percentages(poll_vote.votes, True)

                expiry = "Never"
                if poll_vote.expires_at: 
                    expiry = poll_vote.expires_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]+"Z"

                creation = poll_vote.created_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]+"Z"

                await ws.send_json({
                    "type": "poll_view", 
                    "result_public": poll_vote.is_public,
                    "question": poll_vote.question,
                    "options": poll_vote.options,
                    "votes": poll_vote.votes,
                    "percantage": votes_percantage,
                    "total_votes": sum(poll_vote.votes),
                    "creation": creation,
                    "expiry": expiry,
                })

    except WebSocketDisconnect:
        wsmanager.disconnect(poll_id, ws)



