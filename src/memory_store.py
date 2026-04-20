import json
from datetime import datetime
from src.embedder import get_embedding
from src.database import SessionLocal
from src.models import Memory
from src.graph import build_graph


def calculate_importance(text):
    if "important" in text.lower():
        return 0.9
    return 0.5



def add_memory(user_id, text):
    db=SessionLocal()
    embedding=get_embedding(text).tolist()
    now=str(datetime.now())
    build_graph(text)
    
    new_memory=Memory(
        user_id=user_id,
        text=text,
        embedding=json.dumps(embedding),
        timestamp=now,
        importance=calculate_importance(text),
        access_count=0,
        last_accessed=now
    )
    
    db.add(new_memory)
    db.commit()
    db.close()
    
    
def update_access(memory, db):
    memory.access_count+=1
    memory.impotance=min(memory.importance+0.05,1.0)
    memory.last_accessed=str(datetime.now())
    db.commit()