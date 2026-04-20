import json
import numpy as np
from datetime import datetime
from src.embedder import get_embedding
# from src.memory_store import load_memory
from src.models import Memory
from src.database import SessionLocal
from sklearn.metrics.pairwise import cosine_similarity

# def cosine_similarity(a,b):
#     a=np.array(a)
#     b=np.array(b)
#     return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))

# def retrieve(query, top_k=3):
#     memory=load_memory()
    
#     if len(memory)==0:
#         return []
    
#     query_embedding=get_embedding(query)
    
#     scored_results=[]
    
#     for item in memory:
#         score=cosine_similarity(query_embedding, item["embedding"])
#         scored_results.append((score,item["text"]))
    
#     # Sort by similarity (highest first)  
#     scored_results.sort(key=lambda x:x[0], reverse=True)
    
#     # Return top results
#     return [text for _, text in scored_results[:top_k]]



def apply_decay(memory):
    last=datetime.fromisoformat(memory.last_accessed)
    now=datetime.now()
    days=(now-last).days
    decay=0.01*days
    memory.importance-=decay
    return max(memory.importance, 0.1)




def retrieve(user_id, query, top_k=3):
    db=SessionLocal()
    memories=db.query(Memory).filter(Memory.user_id==user_id).all()
    
    query_emb=get_embedding(query).reshape(1,-1)
    
    scored=[]
    
    for mem in memories:
        emb=np.array(json.loads(mem.embedding)).reshape(1,-1)
        similarity=cosine_similarity(query_emb, emb)[0][0]
        importance=apply_decay(mem)
        
        #Simple recency score
        recency=1/(1+(datetime.now()-datetime.fromisoformat(mem.timestamp)).days)
        
        final_score=(0.6*similarity)+(0.3*importance)+(0.1*recency)
        
        scored.sort(reverse=True, key=lambda x: x[0])
        
    scored.sort(reverse=True, key=lambda x:x[0])
    
    #Reinforce access
    for _, mem in scored[:top_k]:
        update_access(mem, db)
    
    db.close()
    
    return [(score, mem.text) for score, mem in scored[:top_k]]