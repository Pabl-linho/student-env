# endpoint of ws

from fastapi import WebSocket
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # Dictionary to store connections
        # key = user_id
        
        # user rah yfta7o mn multiple devices donc ysra brodcast lihom --[list]--
        
        self.active_connections: Dict[int, List[WebSocket]] = {} 

    async def connect(self, websocket: WebSocket, user_id: int):
        """يتم استدعاؤها لما Flutter يطلب فتح اتصال WebSocket"""
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
            
        self.active_connections[user_id].append(websocket)
        logger.info(f"User {user_id} connected. Total devices: {len(self.active_connections[user_id])}")

    def disconnect(self, websocket: WebSocket, user_id: int): # offline 
        if user_id in self.active_connections:
            try:
                self.active_connections[user_id].remove(websocket)
                # ida 5raj mn all devices removih ml dict ( 3la jal memory leack)

                if len(self.active_connections[user_id]) == 0:
                    del self.active_connections[user_id]
                logger.info(f"User {user_id} disconnected.")

            except ValueError:    # 
                #-------------ws sensible ll connection heavy donc 
                pass

    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(message)

        


    async def broadcast_to_group(self, message: dict, group_members_ids: List[int]):
      
        for user_id in group_members_ids:
            await self.send_personal_message(message, user_id)


manager = ConnectionManager()          # ----- une soule object t3  online users  in the whole app