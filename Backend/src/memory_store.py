import re
import json
import spacy
import numpy as np
from datetime import datetime
from textblob import TextBlob
from src.embedder import get_embedding
from src.database import SessionLocal
from src.models import Memory
from src.graph import build_graph
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")
DUPLICATE_THRESHOLD = 0.75  # lower = catches more near-duplicates

def calculate_importance(text):
    score = 0.5
    if "important" in text.lower():
        score = 0.9
    try:
        sentiment = TextBlob(text).sentiment.polarity
        score += sentiment * 0.1
    except:
        pass
    return min(max(score, 0.1), 1.0)


def is_duplicate(user_id, new_embedding, db):
    """Semantic duplicate detection using embeddings."""
    existing = db.query(Memory).filter(Memory.user_id == user_id).all()
    new_emb = np.array(new_embedding).reshape(1, -1)
    for mem in existing:
        old_emb = np.array(json.loads(mem.embedding)).reshape(1, -1)
        score = cosine_similarity(new_emb, old_emb)[0][0]
        if score > DUPLICATE_THRESHOLD:
            return True
    return False

def clean_text(text):
    """Minimal cleaning — only punctuation and whitespace."""
    text = text.lower().strip()
    text = text.replace("?", "").replace("!", "").replace(",", "")
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def add_memory(user_id, text):
    db = SessionLocal()
    clean = clean_text(text)

    if not clean or len(clean.split()) < 2:
        db.close()
        return


    # Check exact duplicate
    existing = db.query(Memory).filter(
        Memory.user_id == user_id,
        Memory.text == clean
    ).first()
    if existing:
        db.close()
        return

    embedding = get_embedding(clean).tolist()

    # Check semantic duplicate
    if is_duplicate(user_id, embedding, db):
        print(f"Skipping semantic duplicate: {clean}")
        db.close()
        return

    # Also store "my name is X" if "i am X" detected
    name_match = re.search(r'^i am (\w+)$', clean)
    if name_match:
        name = name_match.group(1)
        name_text = f"my name is {name}"
        name_exists = db.query(Memory).filter(
            Memory.user_id == user_id,
            Memory.text == name_text
        ).first()
        if not name_exists:
            name_emb = get_embedding(name_text).tolist()
            now = datetime.now().isoformat()
            db.add(Memory(
                user_id=user_id,
                text=name_text,
                embedding=json.dumps(name_emb),
                timestamp=now,
                importance=0.9,
                access_count=0,
                last_accessed=now
            ))
            db.commit()

    now = datetime.now().isoformat()
    build_graph(clean)

    new_memory = Memory(
        user_id=user_id,
        text=clean,
        embedding=json.dumps(embedding),
        timestamp=now,
        importance=calculate_importance(clean),
        access_count=0,
        last_accessed=now
    )
    db.add(new_memory)
    db.commit()
    db.close()

def update_access(memory, db):
    memory.access_count += 1
    memory.importance = min(memory.importance + 0.05, 1.0)
    memory.last_accessed = str(datetime.now())
    db.commit()