#Sql alchemy models + messages ,groups, chat req, g memberas

import enum
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, Boolean, DateTime, Enum as SQLEnum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


from app.core.database import Base


from app.domains.users.models import User



class ChatType(str, enum.Enum):
    DIRECT = "DIRECT"               
    GROUP = "GROUP"                
    MODULE_COMMUNITY = "MODULE_COMMUNITY"  

class MemberRole(str, enum.Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"

class MessageType(str, enum.Enum):
    TEXT = "TEXT"                     # ATFAKAR bah n5dam b presigned urls (bg)
    IMAGE = "IMAGE"                 
    DOCUMENT = "DOCUMENT"

class RequestStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    chat_type: Mapped[ChatType] = mapped_column(SQLEnum(ChatType), nullable=False)   # single table inhiritance wli m3naha
    # -------------------------- rah ykono messages in db of Direct/ groubs in tthe same table 
    #------------ haka 5ir--- table wa7d fih bazzaf les messages 
    #--- front ra7 yjbd easy

    #?? kayn problem ano ra7 yatarta9 bli message
 
    name: Mapped[str] = mapped_column(String, nullable=True) 
    module_id: Mapped[int] = mapped_column(Integer, nullable=True) # ??
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    #relationships 
    members: Mapped[list["ChatMember"]] = relationship("ChatMember", back_populates="chat", cascade="all, delete-orphan")
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="chat", cascade="all, delete-orphan")


class ChatMember(Base):    
    # tableau li connect users bl chat
    __tablename__ = "chat_members"     # many to Many relation table

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    #------------------ hadi ondelete="CASCADE" fl PostgreSQL ra7 ytm delete auto without orphan

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role: Mapped[MemberRole] = mapped_column(SQLEnum(MemberRole), default=MemberRole.MEMBER)
    #--------------------------------------- const roles i garantee that couldnt modify or back dor $$
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    #relationships
    chat: Mapped["Chat"] = relationship("Chat", back_populates="members")
    user: Mapped["User"] = relationship("User") 


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True) # null if delete 
    content: Mapped[str] = mapped_column(Text, nullable=False)
    message_type: Mapped[MessageType] = mapped_column(SQLEnum(MessageType), default=MessageType.TEXT)
    
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_edited: Mapped[bool] = mapped_column(Boolean, default=False)
    

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    #-------------------------------------------------------------------- in db ra7 yt7t new time of update

    #relationships
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")


class ChatRequest(Base):
    #table t3 add to group or send a req message bah yahadro

    __tablename__ = "chat_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False) 
    
    status: Mapped[RequestStatus] = mapped_column(SQLEnum(RequestStatus), default=RequestStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
