from sqlalchemy import Column, Integer, String, Text, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
from .associations import user_community
from db.database import Base

class Community(Base):
    __tablename__ = "communities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by= Column(Integer,ForeignKey("users.id"),nullable=False)

    users = relationship("User", secondary=user_community, back_populates="communities")
    posts = relationship("Post", back_populates="community")
    creater = relationship("User",back_populates="created_communities")