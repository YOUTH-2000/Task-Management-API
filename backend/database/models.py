from sqlalchemy import Column, Integer,String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.connection import Base
from datetime import datetime


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(255))

    status = Column(String(20))
    priority = Column(String(20))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    hashed_password = Column(String(255))
    role = Column(String(20), default='user')

    tasks = relationship("Task", back_populates="owner")
    