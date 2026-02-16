from typing import Dict, List
from fastapi import WebSocket

class WSConnectionManager: 

    def __init__(self):
        self.rooms: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, poll_id: int, ws: WebSocket):
        if poll_id not in self.rooms: 
            self.rooms[poll_id] = []

        self.rooms[poll_id].append(ws)

    def disconnect(self, poll_id: int, ws: WebSocket):
        self.rooms[poll_id].remove(ws)

        if not self.rooms[poll_id]:
            del self.rooms[poll_id]

    async def broadcast(self, poll_id: int, data: dict):

        if poll_id not in self.rooms:
            return

        for ws in self.rooms[poll_id]:
            await ws.send_json(data)

wsmanager = WSConnectionManager()