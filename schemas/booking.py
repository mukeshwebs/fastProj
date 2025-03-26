from pydantic import BaseModel
from datetime import datetime

class BookingBase(BaseModel):
    status: str = "pending"  # Default status

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    status: str

class BookingResponse(BookingBase):
    id: int
    user_id: int
    session_id: int
    created_at: datetime

    class Config:
        orm_mode = True