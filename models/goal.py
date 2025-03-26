from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
from db.database import Base

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    target_value = Column(Integer, nullable=False)
    current_value = Column(Integer, default=0)
    target_date = Column(DateTime, nullable=False)
    achieved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="goals")
    progress_entries = relationship("Progress", back_populates="goal", cascade="all, delete-orphan")
    achievements = relationship("Achievement", back_populates="goal", cascade="all, delete-orphan")