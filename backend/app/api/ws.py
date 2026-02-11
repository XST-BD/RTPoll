import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException

from sqlalchemy.orm import Session

from app.db.model.poll import PollModel
from app.deps import get_db
from app.setup.ws import wsmanager
from app.setup.cache import redis_client

router = APIRouter()

@router.websocket('/poll/{poll_id}')
async def poll_ws(
    ws: WebSocket, 
    poll_id: int,
    db: Session = Depends(get_db),
):
    
    await wsmanager.connect(poll_id, ws)

    try: 
        # Send initial poll data (like /poll/view)
        votes = redis_client.hgetall(f"poll:{poll_id}:votes")
        poll = db.query(PollModel).filter(PollModel.id==poll_id).first()

        if not poll: 
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

            # Handle refresh 
            if msg_type == "vote":

                option_id: str = data.get("option_id")
                if option_id not in poll.options:

                    await ws.send_json({
                        "type": "error",
                        "message": "Invalid option"
                    })
                    continue

                key = f'poll:{poll_id}:votes'

                # Atomic increment
                new_count = redis_client.hincrby(key, option_id, 1)

                # Broadcast update
                await wsmanager.broadcast(
                    poll_id,
                    {
                        "type": "update",
                        "option_id": option_id,
                        "count": new_count,
                    },
                )

            # Handle vote
            elif msg_type == "get_poll":
                await ws.send_json({
                    "type": "poll_data", 
                    "question": poll.question,
                    "options": poll.options,
                    "votes": poll.votes,
                })
            
            else:
                await ws.send_json({
                    "type": "error", 
                    "message": "Unknown message type",
                })

    except WebSocketDisconnect:
        wsmanager.disconnect(poll_id, ws)


# WS structure (client) | Frontend sends like this
#
#   { type: "join", poll_id:{poll_id:int} }     -> Initiate
#   { type: "get_poll" }                        -> Result
#   { type: "vote", option_id:{option_id:str} } -> Vote 

# WS structure (server) | Frotnend recieves like this 
#
#   { "type": "poll_data", "question": "...", "options": [...], "votes": [...] }
#   { "type": "update", "option_id": "2", "count": 10 }
#   { "type": "error", "message": "Invalid option" }
