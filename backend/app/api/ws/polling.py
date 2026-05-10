from datetime import datetime, timezone
import time
import hashlib

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.concurrency import run_in_threadpool

from app.db.model.poll import PollModel, PollOption
from app.deps import SessionLocal
from app.setup.ws import wsmanager
from app.setup.cache import redis_client 
from app.utils.poll import fetch_poll
from app.utils.vote import verify_token, vote_script

router = APIRouter()


@router.websocket('{poll_id}')
async def poll_status(
    ws: WebSocket,
    poll_id: str,
):
    await ws.accept()
    await wsmanager.connect(poll_id, ws, False)

    token = ws.query_params.get("t")
    fingerprint = str(ws.query_params.get("fp"))

    if token:
        voter_id = verify_token(token)
        if not voter_id:
            await ws.close()
            return
    else: 
        await ws.close()
        return

    if ws.client:
        ip = ws.client.host
    else: 
        await ws.close()
        return

    with SessionLocal() as db:
        try: 
            # Send initial poll data (like /poll/view)

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
            
                    option = await run_in_threadpool(
                        lambda: (db.query(PollOption).filter(PollOption.id == opt_id, PollOption.poll_id == poll_id).first())
                    )
                    
                    if not option or option.id != opt_id:
                        await ws.send_json({"type": "error", "message": "Invalid option"})
                        continue

                    voter_key = f"poll:{poll_id}:voter:{voter_id}"
                    votes_key = f"poll:{poll_id}:votes"

                    fp_hash = hashlib.sha256(fingerprint.encode()).hexdigest()

                    fp_key = f"poll:{poll_id}:fp:{fp_hash}:10s"
                    ip_key = f"poll:{poll_id}:ip:{ip}:10s"
                    block_key = f"poll:{poll_id}:fp:{fp_hash}:blocked"

                    result = vote_script.execute(
                        keys=[voter_key, votes_key, fp_key, ip_key, block_key],
                        args=[opt_id, int(time.time()), 5, 10, 30]
                    )

                    status = result[0]

                    if status == "blocked":
                        await ws.send_json({"type": "error", "message": "Temporarily blocked"})
                        continue

                    elif status == "cooldown":
                        await ws.send_json({"type": "notice", "message": "Too many votes. Slow down."})
                        continue

                    elif status == "no-op":
                        await ws.send_json({"type": "notice", "message": "Already voted for this option"})
                        continue

                    elif status == "ok":
                        votes = await redis_client.hgetall(votes_key)   # type: ignore
                        votes = {str(k): int(v) for k, v in votes.items()}

                        await wsmanager.broadcast(poll_id=poll_id,  payload={"type": "results", "votes": votes})

        except WebSocketDisconnect:
            wsmanager.disconnect(poll_id, ws)