from pydantic import BaseModel
from datetime import datetime

class ProgressBase(BaseModel):
    value: int
    note: str | None = None

class ProgressCreate(ProgressBase):
    pass

class ProgressResponse(ProgressBase):
    id: int
    goal_id: int
    created_at: datetime

    class Config:
        orm_mode = True