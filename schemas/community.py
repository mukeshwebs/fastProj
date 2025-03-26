from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CommunityBase(BaseModel):
    name: str
    description: Optional[str] = None

#  Schema for creating a new community (Request)
class CommunityCreate(CommunityBase):
    pass

#  Schema for updating a community (Request)
class CommunityUpdate(CommunityBase):
    pass

#  Schema for retrieving a community (Response)
class CommunityResponse(CommunityBase):
    id: int
    created_at: datetime
    created_by: int
    user_ids: List[int] = []
    
    class Config:
        from_attributes = True  # Enables ORM compatibility