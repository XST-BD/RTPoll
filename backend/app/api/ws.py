import asyncio

from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException

from jose import JWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.model.poll import PollModel
from app.db.model.user import UserModel
from app.deps import get_db, session_local
from app.services.auth import decode_token
from app.setup.ws import wsmanager
from app.setup.cache import redis_client 
from app.setup.vars import FRONTEND_URL

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

# async def build_poll_response(poll: PollModel) -> PollResponseModel:
#     if not poll:
#         raise ValueError("Poll not found")

#     total_votes = sum(poll.votes)  # sum integers from votes list
#     options = poll.options  # already a list[str]

#     # Handle expires_at safely
#     expires_at: datetime | str
#     if poll.is_indefinite or poll.expires_at is None:
#         expires_at = "Never"
#     else:
#         expires_at = poll.expires_at

#     return PollResponseModel(
#         id=poll.id,
#         question=poll.question,
#         options=options,
#         total_votes=total_votes,
#         expires_at=expires_at
#     )


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

                await ws.send_json({
                    "type": "vote_data", 
                    "question": poll_vote.question,
                    "options": poll_vote.options,
                    "votes": poll_vote.votes,
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

            await ws.send_json({
                "type": "poll_view", 
                "question": poll_vote.question,
                "options": poll_vote.options,
                "votes": poll_vote.votes,
                "total_votes": sum(poll_vote.votes),
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

                await ws.send_json({
                    "type": "poll_view", 
                    "question": poll_vote.question,
                    "options": poll_vote.options,
                    "votes": poll_vote.votes,
                    "total_votes": sum(poll_vote.votes),
                })

    except WebSocketDisconnect:
        wsmanager.disconnect(poll_id, ws)

# For endpoint: ws://127.0.0.1:8000/ws/poll/{poll_id}

# Send: {type: "poll_view"}  
# Recieve: {type:"Poll data", question:str, options:[str], votes:[int]}


# For endpoint: ws://127.0.0.1:8000/ws/vote/{poll_id}

# Send: {type: "get_vote"}
# Recieve: {type: "vote_data", question:str, options:[str], votes:[int]}

# Send: {type: "send_vote", option_id: str}
# Recieve: {'type': 'vote_update', 'option_id': str, 'count': int}


