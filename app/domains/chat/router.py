from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect   , HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.domains.chat import schemas

from app.domains.chat.websocket import manager
from app.domains.chat.service import ChatService


async def get_current_user(user_id: int = 1) -> int:
    return user_id
# ---------------------------------------hna

router = APIRouter(prefix="/chat", tags=["Chat System"])




@router.get("/{chat_id}/messages", response_model=List[schemas.MessageResponse])
async def get_chat_history(
    chat_id: int, 
    limit: int = 40, 
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user) 
):
    messages = await ChatService.get_chat_history(
        db=db, 
        chat_id=chat_id, 
        user_id=current_user_id, 
        limit=limit, 
        offset=offset
    )
    return messages



@router.websocket("/ws/{chat_id}")
async def websocket_chat_endpoint(
    websocket: WebSocket, 
    chat_id: int,

    user_id: int, 
    db: AsyncSession = Depends(get_db)
):
    try:
       
        await ChatService.verify_user_in_chat(db, chat_id, user_id)
    except HTTPException:
        await websocket.close(code=1008)
        return

    await manager.connect(websocket, user_id)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            try:
                message_data = schemas.MessageCreate(**data, chat_id=chat_id)
                new_message = await ChatService.create_message(
                    db=db, 
                    chat_id=chat_id, 
                    sender_id=user_id, 
                    message_data=message_data
                )
                
                response_schema = schemas.MessageResponse.model_validate(new_message)
                response_dict = response_schema.model_dump(mode='json')
                members_ids = await ChatService.get_chat_members_ids(db, chat_id)
                await manager.broadcast_to_group(response_dict, members_ids)

            except Exception as e:
                await websocket.send_json({"error": str(e)})

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)