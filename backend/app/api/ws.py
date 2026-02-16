import asyncio

from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.model.poll import PollModel
from app.deps import get_db, session_local
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

async def build_poll_response(poll):
    return PollResponseModel.model_validate(poll)

async def get_current_user_ws(ws: WebSocket):
    session = ws.scope.get("session")

    if not session:
        return None 
    
    user_id = session.get("user_id")
    if not user_id: 
        return None 



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
        # votes = redis_client.hgetall(f"poll:{poll_id}:votes")
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


@router.websocket('/poll/{poll_id}')
async def poll_ws(
    ws: WebSocket, 
    poll_id: int, 
    db: Session = Depends(get_db),
):
    await ws.accept()
    await wsmanager.connect(poll_id, ws)

    try: 
        # send initial poll data 
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

            # ================================= POLL ================================= #

            if msg_type == "poll_view":

                db = session_local
                poll_view = db.get(PollModel, poll_id)

                if poll_view is None: 
                    await ws.send_json({
                        "type": "error", 
                        "message": "Poll not found",
                    })
                    return
                
                user = await get_current_user_ws(ws)

                if user is None or not user: 
                    await ws.send_json({
                        "type": "error", 
                        "message": "User not found or unauthorized",
                    })
                    await ws.close(code=1008)   # Policy violation
                    return
                    
                await ws.accept()

                response = await build_poll_response(poll_view)
                await ws.send_json({
                    "type": f"poll_data_{poll_id}",
                    "data": response,
                })
            
            else:
                await ws.send_json({
                    "type": "error", 
                    "message": "Unknown message type",
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


