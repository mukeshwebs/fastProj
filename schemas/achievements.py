from pydantic import BaseModel
from datetime import datetime

class AchievementBase(BaseModel):
    title: str
    description: str | None = None

class AchievementCreate(AchievementBase):
    pass

class AchievementResponse(AchievementBase):
    id: int
    goal_id: int
    achieved_at: datetime

    class Config:
        orm_mode = True