from pydantic import BaseModel
from datetime import datetime

#  Comment Create Schema
class CommentCreate(BaseModel):
    content: str

# Comment Update Schema
class CommentUpdate(BaseModel):
    content: str

#  Comment Response Schema
class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    user_id: int
    post_id: int

    class Config:
        orm_mode = True