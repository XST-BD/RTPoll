from typing import Dict, List, Optional
from fastapi import WebSocket

class WSConnectionManager: 

    def __init__(self):
        self.rooms: Dict[str, List[WebSocket]] = {}
        self.ws: WebSocket

    async def connect(self, poll_id: str, ws: WebSocket, is_creator: bool):
        if poll_id not in self.rooms: 
            self.rooms[poll_id] = []

        self.rooms[poll_id].append(ws)

    def disconnect(self, poll_id: str, ws: WebSocket):
        if poll_id not in self.rooms: 
            return
        
        self.rooms[poll_id] = [w for w in self.rooms[poll_id] if w != ws]

        if not self.rooms[poll_id]:
            del self.rooms[poll_id] 

    async def broadcast(self, poll_id: str, payload):

        if poll_id not in self.rooms:
            return

        for ws in self.rooms[poll_id]:
            await ws.send_json(payload)

wsmanager = WSConnectionManager()