import json
import numpy as np
from datetime import datetime
from src.embedder import get_embedding
from src.models import Memory
from src.memory_store import update_access
from src.database import SessionLocal
from src.graph import expand_query
from sklearn.metrics.pairwise import cosine_similarity


def apply_decay(memory):
    last=datetime.fromisoformat(memory.last_accessed)
    now=datetime.now()
    days=(now-last).days
    decay=0.01*days
    memory.importance-=decay
    return max(memory.importance, 0.1)


def extract_keywords(text):
    stopwords = {"what", "is", "are", "the", "a", "an", "do", "i", "you", "me", "my"}
    words = text.lower().split()
    return [w for w in words if w not in stopwords]


def retrieve(user_id, query, top_k=1):
    query=expand_query(query)
    db=SessionLocal()
    memories=db.query(Memory).filter(Memory.user_id==user_id).all()
    
    query_emb=get_embedding(query).reshape(1,-1)
    
    scored=[]
    
    for mem in memories:
        emb = np.array(json.loads(mem.embedding)).reshape(1, -1)
        similarity = cosine_similarity(query_emb, emb)[0][0]
        importance = apply_decay(mem)

        recency = 1 / (1 + (datetime.now() - datetime.fromisoformat(mem.timestamp)).days)

        keyword_score = 0
        query_keywords = extract_keywords(query)
        for word in query_keywords:
            mem_words = mem.text.lower().split()
            if word in mem_words:
                keyword_score += 0.1

        final_score = (
            0.5 * similarity +
            0.3 * importance +
            0.1 * recency +
            0.1 * keyword_score
        )

        scored.append((final_score, mem))
        
    scored.sort(reverse=True, key=lambda x: x[0])

    filtered = [(score, mem) for score, mem in scored if score > 0.5]

    if not filtered:
        db.close()
        return []

    top_results = filtered[:top_k]
    
    

    for _, mem in top_results:
        update_access(mem, db)
     
    results=[]
    for score, mem in top_results:
        results.append((score, mem.text))

    db.close()
    return results