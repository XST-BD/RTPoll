from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException

from sqlalchemy.orm import Session

from app.db.model.poll import PollModel
from app.service import wsmanager, get_db
from app.setup.cache import redis_client

router = APIRouter()

@router.websocket('/poll/{poll_id}')
async def poll_ws(
    websocket: WebSocket, 
    poll_id: int,
    db: Session = Depends(get_db),
):
    
    await wsmanager.connect(poll_id, websocket)

    try: 
        # send initial state
        votes = redis_client.hgetall(f"poll:{poll_id}:votes")
        poll = db.query(PollModel).filter(PollModel.id==poll_id).first()

        if poll is None: 
            raise HTTPException(404, "Poll not found")

        await websocket.send_json({"type": "init", "options": poll.options, "votes": votes})

        while True: 
            await websocket.receive_text()

    except WebSocketDisconnect:
        wsmanager.disconnect(poll_id, websocket)


