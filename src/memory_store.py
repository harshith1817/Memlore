import json
import os
from datetime import datetime
from src.embedder import get_embedding

MEMORY_FILE="data/memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)
    
def add_memory(text):
    memory=load_memory()
    embedding=get_embedding(text)
    
    new_entry={
        "text": text,
        "embedding": embedding.tolist(),
        "timestamp": str(datetime.now())
    }
    
    memory.append(new_entry)
    save_memory(memory)
    
    return "Memory stored successfully!"