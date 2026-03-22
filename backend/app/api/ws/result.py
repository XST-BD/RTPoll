from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.deps import SessionLocal
from app.services.auth import validate_ws_user
from app.setup.cache import redis_client
from app.setup.ws import wsmanager

router = APIRouter()

@router.websocket('/poll/{poll_id}/result')
async def poll_result_ws(ws: WebSocket, poll_id: str):
    
    await ws.accept()
    db = SessionLocal()

    user = None

    try:
        data = await ws.receive_json()
        token = data.get('token')
        msg_type = data.get('type')

        # auth
        await validate_ws_user(db, user, poll_id, token, ws)

        #handle message

    except WebSocketDisconnect:
        wsmanager.disconnect(poll_id, ws)

    finally:
        db.close()