from sqlalchemy import Column, Integer, String, ForeignKey
from src.database import Base

class Memory(Base):
    __tablename__="memories"
    
    id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer, ForeignKey("users.id"))
    text=Column(String)
    embedding=Column(String)
    timestamp=Column(String)
    
class User(Base):
    __tablename__="users"
    
    id=Column(Integer, primary_key=True, index=True)
    email=Column(String, unique=True)
    password=Column(String)