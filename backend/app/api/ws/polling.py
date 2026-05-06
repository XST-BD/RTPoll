from datetime import datetime, timezone

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.concurrency import run_in_threadpool

from pydantic import BaseModel

from app.db.model.poll import PollModel, PollOption
from app.deps import SessionLocal
from app.setup.ws import wsmanager
from app.setup.cache import redis_client 
from app.utils.ws import transform_for_creator, transform_for_voter
from app.utils.poll import fetch_poll

router = APIRouter()

class PollResponseModel(BaseModel):
    poll_id: int 
    opt_id: int
    votes: int 

    class Config:
        from_attributes = True


@router.websocket('{poll_id}')
async def poll_status(
    ws: WebSocket,
    poll_id: str,
):
    await ws.accept()
    await wsmanager.connect(poll_id, ws, False)

    try: 
        # Send initial poll data (like /poll/view)
        db = SessionLocal()
        poll = db.query(PollModel).filter(PollModel.id==poll_id).first()

        if poll is None: 
            await ws.send_json({"type": "error", "message": "Poll not found"})
            return
        
        while True: 
            data = await ws.receive_json()
            msg_type = data.get("type")

            if msg_type == "info":
                try: 
                    poll_vote = await run_in_threadpool(lambda: fetch_poll(poll_id))

                    if poll_vote is None: 
                        await ws.send_json({"type": "error", "message": "Poll not found"})
                        continue

                    if poll_vote.expires_at and poll_vote.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc): 
                        await ws.send_json({"type": "notice", "message": "This poll has ended"})
                        continue    
                        
                    # Read live votes from Redis
                    key = f'poll:{poll_id}:votes'
                    await ws.send_json({"type": "info", "opt_id": poll})
                except Exception as e:
                    # Catch everything so the WS doesn’t disconnect
                    await ws.send_json({"type": "error", "message": str(e)})

                finally: 
                    db.close()

            elif msg_type == "update":
                db = SessionLocal()
                
                try:
                    poll_vote = await run_in_threadpool(db.get, PollModel, poll_id)

                    if not poll_vote: 
                        await ws.send_json({"type": "error", "message": "Poll not found"})
                        continue
                
                    if poll_vote.expires_at and poll_vote.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc): 
                        await ws.send_json({"type": "notice", "message": "This poll has ended"})
                        continue

                    try:
                        option_id = str(data.get("option_id"))
                    except (TypeError, ValueError):
                        await ws.send_json({"type": "error", "message": "Invalid option"})
                        continue
            
                    option = await run_in_threadpool(db.get, PollOption, option_id)
                    if not option or option.id != option_id:
                        await ws.send_json({"type": "error", "message": "Invalid option"})
                        continue

                    key = f'poll:{poll_id}:votes'

                    # Atomic increment
                    await redis_client.hincrby(key, str(option_id), 1) # type: ignore

                    # Read live votes from Redis
                    redis_votes = await redis_client.hgetall(key) # type: ignore
                    redis_votes = {str(k): int(v) for k, v in redis_votes.items()} # Convert to {option_id: count}

                    voter_payload = await transform_for_voter("vote_update", key, poll_vote)
                    creator_payload = await transform_for_creator("vote_update", key, poll_vote)
                   
                    await wsmanager.broadcast(
                        poll_id,
                        voter_payload=voter_payload,
                        creator_payload=creator_payload,
                    )
                finally: 
                    db.close()



    except WebSocketDisconnect:
        wsmanager.disconnect(poll_id, ws)