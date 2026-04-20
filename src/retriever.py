import json
import numpy as np
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

def retrieve(user_id, query, top_k=3):
    db=SessionLocal()
    memories=db.query(Memory).filter(Memory.user_id==user_id).all()
    db.close()
    
    query_emb=get_embedding(query).reshape(1,-1)
    
    scored=[]
    
    for mem in memories:
        emb=np.array(json.loads(mem.embedding)).reshape(1,-1)
        score=cosine_similarity(query_emb, emb)[0][0]
        scored.append((score, mem.text))
        
    scored.sort(reverse=True)
    return scored[:top_k]