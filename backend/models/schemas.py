"""
Pydantic Schemas - Data validation models for API requests and responses
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ChatMode(str, Enum):
    """Chat mode enumeration"""
    AUTO = "auto"
    OFFLINE = "offline"
    ONLINE = "online"


class UserBase(BaseModel):
    """Base user schema"""
    user_id: str = Field(..., description="Unique user identifier")
    name: Optional[str] = Field(None, description="User's name")


class UserCreate(UserBase):
    """Schema for creating a new user"""
    pass


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    created_at: datetime
    last_active: datetime

    class Config:
        from_attributes = True


class ChatMessage(BaseModel):
    """Chat message schema"""
    message: str = Field(..., min_length=1, max_length=5000, description="User's message")
    user_id: str = Field(..., description="User identifier")
    mode: Optional[str] = Field("auto", description="Chat mode: auto, offline, or online")


class ChatMessageResponse(BaseModel):
    """Response schema for chat messages"""
    response: str = Field(..., description="AI's response")
    mode: str = Field(..., description="Mode used to generate response")
    synced: bool = Field(False, description="Whether the message is synced to cloud")


class ChatHistoryItem(BaseModel):
    """Individual chat history item"""
    id: int
    user_id: str
    message: str
    response: str
    mode: str
    timestamp: datetime
    synced: bool

    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """Response schema for chat history"""
    user_id: str
    chats: List[ChatHistoryItem]
    total: int


class SyncRequest(BaseModel):
    """Request schema for data synchronization"""
    force_sync: bool = Field(False, description="Force sync even if there are conflicts")


class SyncResponse(BaseModel):
    """Response schema for sync operations"""
    success: bool
    message: str
    synced_count: int = 0
    pending_sync: Optional[int] = None


class SyncStatus(BaseModel):
    """Sync status information"""
    pending_count: int
    is_online: bool
    last_sync: Optional[datetime] = None
    error: Optional[str] = None


class HealthCheck(BaseModel):
    """Health check response"""
    name: str
    version: str
    status: str
    connectivity: bool


class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
