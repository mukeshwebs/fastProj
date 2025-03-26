from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Request schema for creating a session
class SessionCreate(BaseModel):
    title: str
    description: Optional[str] = None
    scheduled_at: datetime


# Response schema for session details
class SessionResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    scheduled_at: datetime
    program_id: int
    created_by: int

    class Config:
        from_attributes = True