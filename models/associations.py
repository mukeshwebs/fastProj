from sqlalchemy import Table, Column, Integer, ForeignKey
from .base import Base
from db.database import Base

user_program = Table(
    "user_program",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("program_id", Integer, ForeignKey("programs.id"), primary_key=True),
)

user_community = Table(
    "user_community",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("community_id", Integer, ForeignKey("communities.id"), primary_key=True),
)