from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from db.database import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    scheduled_at = Column(DateTime, nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id"))
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    program = relationship("Program", back_populates="sessions")
    creator = relationship("User", back_populates="created_sessions")

    bookings =relationship("Booking",back_populates="session",cascade="all,delete")