from sqlalchemy import Column, Integer,  Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
from db.database import Base

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False)
    value = Column(Integer, nullable=False)
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    goal = relationship("Goal", back_populates="progress_entries")