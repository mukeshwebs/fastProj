from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class PostBase(BaseModel):
    content: str

# ✅ Schema for creating a new post
class PostCreate(PostBase):
    pass

# ✅ Schema for updating a post
class PostUpdate(PostBase):
    pass

# ✅ Schema for retrieving a post
class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    community_id: int
    
    class Config:
        from_attributes = True  # Enables ORM compatibility