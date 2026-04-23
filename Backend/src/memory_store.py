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
    clean_text = text.lower().replace("?", "").strip()
    
    existing = db.query(Memory).filter(
        Memory.user_id == user_id,
        Memory.text == clean_text
    ).first()
    
    if existing:
        db.close()
        return
    
    embedding=get_embedding(clean_text).tolist()
    now=datetime.now().isoformat()
    build_graph(text)
    
    new_memory=Memory(
        user_id=user_id,
        text=clean_text,
        embedding=json.dumps(embedding),
        timestamp=now,
        importance=calculate_importance(clean_text),
        access_count=0,
        last_accessed=now
    )
    
    db.add(new_memory)
    db.commit()
    db.close()
    
    
def update_access(memory, db):
    memory.access_count+=1
    memory.importance=min(memory.importance+0.05,1.0)
    memory.last_accessed=str(datetime.now())
    db.commit()