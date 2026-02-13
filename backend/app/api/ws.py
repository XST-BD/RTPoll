import asyncio

from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.model.poll import PollModel
from app.deps import get_db
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
        
        await ws.send_json({
            "type": "Poll data", 
            "question": poll.question,
            "options": poll.options,
            "votes": poll.votes,
        })

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

                option_id: str = data.get("option_id")
                if option_id not in poll.options:

                    await ws.send_json({
                        "type": "error",
                        "message": "Invalid option",
                    })
                    continue

                key = f'poll:{poll_id}:votes'

                # Atomic increment
                new_count = redis_client.hincrby(key, option_id, 1)

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
                await ws.send_json({
                    "type": "vote_data", 
                    "question": poll.question,
                    "options": poll.options,
                    "votes": poll.votes,
                })

    except WebSocketDisconnect:
        wsmanager.disconnect(poll_id, ws)


@router.websocket('poll/{poll_id}')
async def poll_ws(
    ws: WebSocket, 
    poll_id: int, 
    db: Session = Depends(get_db),
):
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

        await ws.send_json({
            "type": "Poll data", 
            "question": poll.question,
            "options": poll.options,
            "votes": poll.votes,
        }) 

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

                user = await get_current_user_ws(ws)

                if user is None or not user: 
                    await ws.close(code=1008)   # Policy violation
                    
                await ws.accept()

                response = await build_poll_response(poll)
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

# WS vote structure (client) | Frontend sends like this
#
#   { type: "join", poll_id:{poll_id:int} }     -> Initiate
#   { type: "get_vote" }                        -> Result
#   { type: "send_vote", option_id:{option_id:str} } -> Vote 

# WS vote structure (server) | Frotnend recieves like this 
#
#   { "type": "vote_data", "question": "...", "options": [...], "votes": [...] }
#   { "type": "vote_update", "option_id": "2", "count": 10 }
#   { "type": "error", "message": "Invalid option" }


# Workflow (vote)
# send_type: get_vote, get_type: vote_data 
# send_type: send_vote, get_type: vote_update 


# WS poll structure (client) | Frontend sends like this 
#   
#   { type: "poll_view_all" }                       -> Get all poll overview created by user
#   { type: "poll_view", poll_id:{poll_id:int} }    -> Get specific poll

# WS poll structure (server) | Frontend recieves like this 
#
#   { 
#       type: "poll_data_{poll_id:int}", 
#       question: {question:str}, 
#       options: [str], 
#       total_votes: {total_votes:int}, 
#       votes: [int],  
#       expires_at:  {expires_at:datetime}
#   }    
#   -> Get specific poll

# Workflow (poll)
# send_type: poll_view, get_type: poll_data_{poll_id:int}



