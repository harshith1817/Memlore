import numpy as np
from src.embedder import get_embedding
from src.memory_store import load_memory

def cosine_similarity(a,b):
    a=np.array(a)
    b=np.array(b)
    return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve(query, top_k=3):
    memory=load_memory()
    
    if len(memory)==0:
        return []
    
    query_embedding=get_embedding(query)
    
    scored_results=[]
    
    for item in memory:
        score=cosine_similarity(query_embedding, item["embedding"])
        scored_results.append((score,item["text"]))
    
    # Sort by similarity (highest first)  
    scored_results.sort(key=lambda x:x[0], reverse=True)
    
    # Return top results
    return [text for _, text in scored_results[:top_k]]