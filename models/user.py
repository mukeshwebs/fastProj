from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
from .associations import user_program, user_community
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String,nullable=False,default="user")
    created_at = Column(DateTime, default=datetime.utcnow)

    programs = relationship("Program", secondary=user_program, back_populates="users")
    communities = relationship("Community", secondary=user_community, back_populates="users")
    posts = relationship("Post", back_populates="user")
    likes = relationship("Like", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    created_programs = relationship("Program", back_populates="creator")
    created_sessions = relationship("Session", back_populates="creator")

    goals = relationship("Goal",back_populates="user",cascade="all,delete-orphan")
    bookings = relationship("Booking",back_populates="user",cascade="all,delete-orphan")
    #payments = relationship("Payment",back_populates="user",cascade="all,delete-orphan")
    #nutrition_logs = relationship("Nutrition",back_populates="user",cascade="all,delete-orphan")

    created_communities = relationship("Community", back_populates="creater")