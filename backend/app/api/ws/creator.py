from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from fastapi.concurrency import run_in_threadpool

from jose import JWTError

from app.db.model.user import UserModel
from app.deps import get_db, SessionLocal
from app.services.auth import decode_token
from app.setup.ws import wsmanager
from app.setup.cache import redis_client 
from app.utils import create_payload, fetch_poll

router = APIRouter()

@router.websocket("/poll/{poll_id}")
async def poll_ws(ws: WebSocket, poll_id: int):
    await ws.accept()

    db = SessionLocal()

    try:
        user = None  # auth state

        while True:
            data = await ws.receive_json()

            token = data.get("token")
            msg_type = data.get("type")

            # ================= AUTH (run once) =================
            if not user:
                if not token:
                    await ws.send_json({
                        "type": "error",
                        "message": "Missing access token"
                    })
                    await ws.close(code=1008)
                    return

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

                    await wsmanager.connect(poll_id, ws, True)

                except JWTError:
                    await ws.send_json({
                        "type": "error",
                        "message": "Invalid token"
                    })
                    await ws.close(code=1008)
                    return

            # ================= HANDLE MESSAGE =================
            if msg_type == "poll_view":
                try:
                    poll_vote = await run_in_threadpool(lambda: fetch_poll(poll_id))

                    if poll_vote is None:
                        await ws.send_json({
                            "type": "error",
                            "message": "Poll not found"
                        })
                        continue

                    key = f'poll:{poll_id}:votes'
                    payload = await create_payload("poll_view", key, poll_vote)

                    await ws.send_json(payload)

                except Exception as e:
                    await ws.send_json({"type": "error", "message": str(e)})

    except WebSocketDisconnect:
        wsmanager.disconnect(poll_id, ws)

    finally:
        db.close()


