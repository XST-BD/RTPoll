from datetime import datetime, timezone

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.concurrency import run_in_threadpool

from app.db.model.poll import PollModel, PollOption
from app.deps import SessionLocal
from app.setup.ws import wsmanager
from app.setup.cache import redis_client 
from app.utils.poll import fetch_poll

router = APIRouter()


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
                    opt_id = str(data.get("opt_id"))

                    if poll_vote is None: 
                        await ws.send_json({"type": "error", "message": "Poll not found"})
                        continue

                    if poll_vote.expires_at and poll_vote.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc): 
                        await ws.send_json({"type": "notice", "message": "This poll has ended"})
                        continue    
                        
                    # Read live votes from Redis
                    key = f'poll:{poll_id}:{opt_id}'
                    vote_count = redis_client.hgetall(key)
                    await ws.send_json({"type": "info", "opt_id": opt_id, "votes": vote_count})
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
                        opt_id = str(data.get("option_id"))
                    except (TypeError, ValueError):
                        await ws.send_json({"type": "error", "message": "Invalid option"})
                        continue
            
                    option = await run_in_threadpool(db.get, PollOption, opt_id)
                    if not option or option.id != opt_id:
                        await ws.send_json({"type": "error", "message": "Invalid option"})
                        continue

                    key = f'poll:{poll_id}:{opt_id}'

                    # Atomic increment
                    await redis_client.hincrby(key, str(opt_id), 1) # type: ignore

                    # Read live votes from Redis
                    redis_votes = await redis_client.hgetall(key) # type: ignore
                    redis_votes = {str(k): int(v) for k, v in redis_votes.items()} # Convert to {option_id: count}

                    await ws.send_json({"type": "update", "message": "Poll updated"})

                finally: 
                    db.close()

    except WebSocketDisconnect:
        wsmanager.disconnect(poll_id, ws)