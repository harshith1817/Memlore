from sqlalchemy import Column, Integer, String
from src.database import Base

class Memory(Base):
    __tablename__="memories"
    
    id=Column(Integer, primary_key=True, index=True)
    text=Column(String)
    embedding=Column(String)
    timestamp=Column(String)