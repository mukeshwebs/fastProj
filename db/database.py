from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

DATABASE_URL = "postgresql://postgres:restart?#x6666@localhost:5432/mydb"

# Create engine
engine = create_engine(DATABASE_URL)

# Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Import models at the top to register them
from models.user import User
from models.program import Program
from models.session import Session
from models.community import Community
from models.post import Post
from models.like import Like
from models.comment import Comment

# Function to create database tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()