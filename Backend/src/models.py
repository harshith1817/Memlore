from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text, DateTime
from datetime import datetime
from src.database import Base

class Memory(Base):
    __tablename__="memories"
    
    id=Column(Integer, primary_key=True, index=True)
    user_id=Column(String, ForeignKey("users.id"))
    
    text=Column(Text)
    embedding=Column(String)
    
    timestamp=Column(DateTime, default=datetime.utcnow)
    importance=Column(Float)
    access_count=Column(Integer)
    last_accessed=Column(DateTime)
    
class User(Base):
    __tablename__="users"
    
    id=Column(String, primary_key=True)
    email=Column(String, unique=True)
    password=Column(String)