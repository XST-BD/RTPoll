from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.concurrency import run_in_threadpool

from app.deps import SessionLocal
from app.services.auth import validate_ws_user
from app.setup.ws import wsmanager
from app.utils.poll import fetch_poll
from app.utils.ws import transform_for_creator

router = APIRouter()

@router.websocket("/poll/{poll_id}")
async def poll_ws(ws: WebSocket, poll_id: str):
    
    await ws.accept()
    db = SessionLocal()

    try:
        user = None  # auth state

        while True:
            data = await ws.receive_json()
            token = data.get("token")
            msg_type = data.get("type")

            # auth
            await validate_ws_user(db, user, poll_id, token, ws)

            # handle message
            if msg_type == "poll_view":
                try:
                    poll_vote = await run_in_threadpool(lambda: fetch_poll(poll_id))

                    if poll_vote is None:
                        await ws.send_json({"type": "error", "message": "Poll not found"})
                        continue

                    key = f'poll:{poll_id}:votes'
                    payload = await transform_for_creator("poll_view", key, poll_vote)

                    await ws.send_json(payload)

                except Exception as e:
                    print(f"WS Error: {str(e)}")

    except WebSocketDisconnect:
        wsmanager.disconnect(poll_id, ws)

    finally:
        db.close()


