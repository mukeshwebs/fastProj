from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Request schema for creating a program
class ProgramCreate(BaseModel):
    name: str
    description: Optional[str] = None

# Response schema for program details
class ProgramResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    created_by: int

    class Config:
        from_attributes = True