from pydantic import BaseModel
from datetime import datetime

class GoalBase(BaseModel):
    title: str
    description: str | None = None
    target_value: int
    current_value: int = 0
    target_date: datetime

class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    current_value: int | None = None
    target_value: int | None = None
    achieved: bool | None = None

class GoalResponse(GoalBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True