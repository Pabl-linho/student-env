from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

# نجبدو الـ Enums لي كرييناهم في الـ Models باش نستعملوهم للـ Validation
from app.domains.chat.models import ChatType, MessageType, MemberRole, RequestStatus


class MessageBase(BaseModel):
#------------------------------- nadamno ano all messages has content + type( text or t3 upload and imojis rahom text)

    content: str = Field(..., description="message content ")
    message_type: MessageType = Field(default=MessageType.TEXT)

class MessageCreate(MessageBase):
    #                                    ml front yoslni chat-id """
    chat_id: int

class MessageResponse(MessageBase):
    #------------------------------------- API t3 JSON Response to front 
    id: int
    chat_id: int
    sender_id: Optional[int] #??
    is_edited: bool
    is_deleted: bool
    created_at: datetime
    updated_at: Optional[datetime]








    model_config = ConfigDict(from_attributes=True)

class ChatBase(BaseModel):
    chat_type: ChatType
    name: Optional[str] = Field(None, description=" group name ( rah ykon empty fl direct chat)")
    module_id: Optional[int] = Field(None, description="t3 communities")

class ChatCreate(ChatBase):
    
    contact_id: Optional[int] = None 
    
class ChatResponse(ChatBase):
    id: int
    created_at: datetime         # ??
    
    model_config = ConfigDict(from_attributes=True)


class ChatRequestBase(BaseModel):
    chat_id: int

class ChatRequestCreate(ChatRequestBase):
    """الطالب يبعث طلب باش يدخل لجروب أو يهدر مع Contact"""
    receiver_id: int

class ChatRequestResponse(ChatRequestBase):
    id: int
    sender_id: int
    receiver_id: int
    status: RequestStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)