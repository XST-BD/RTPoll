from typing import Dict, List, Optional
from fastapi import WebSocket

class WSConnectionManager: 

    def __init__(self):
        self.rooms: Dict[int, List[tuple[WebSocket, bool]]] = {}
    
    async def connect(self, poll_id: int, ws: WebSocket, is_creator: bool):
        if poll_id not in self.rooms: 
            self.rooms[poll_id] = []

        self.rooms[poll_id].append((ws, is_creator))

    def disconnect(self, poll_id: int, ws: WebSocket):
        if poll_id not in self.rooms: 
            return
        
        self.rooms[poll_id] = [(w, c) for (w, c) in self.rooms[poll_id] if w != ws]

        if not self.rooms[poll_id]:
            del self.rooms[poll_id] 

    async def broadcast(
        self, 
        poll_id: int, 
        voter_payload,
        creator_payload,
    ):
        if poll_id not in self.rooms: 
            return 

        for ws, is_creator in self.rooms[poll_id]:
            payload = creator_payload if is_creator else voter_payload
        
            if payload is None:
                continue

            try: 
                await ws.send_json(payload)
            except: 
                self.disconnect(poll_id, ws)

wsmanager = WSConnectionManager()