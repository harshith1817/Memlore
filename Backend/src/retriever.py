import json
import numpy as np
from datetime import datetime
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from src.embedder import get_embedding
from src.models import Memory
from src.memory_store import update_access
from src.database import SessionLocal
from src.graph import expand_query
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import DateTime


nlp = spacy.load("en_core_web_sm")
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

STOPWORDS = set(stopwords.words('english'))

def apply_decay(memory):
    now = datetime.now()
    if isinstance(memory.last_accessed, str):
        last = datetime.fromisoformat(memory.last_accessed)
    elif isinstance(memory.last_accessed, datetime):
        last = memory.last_accessed
    else:
        last = now
    days = (now - last).days
    decay = 0.01 * days
    memory.importance -= decay
    return max(memory.importance, 0.1)


def extract_keywords(text):
    """NLTK-based keyword extraction — much better than manual."""
    tokens = word_tokenize(text.lower())
    return [w for w in tokens if w.isalpha() and w not in STOPWORDS]


def tokenize(text):
    doc = nlp(text.lower())
    return [
        token.lemma_
        for token in doc
        if token.is_alpha and token.lemma_ not in ["be", "do", "have"]
    ]
    
    
def retrieve(user_id, query, top_k=3):
    expanded = expand_query(query)
    db = SessionLocal()
    memories = db.query(Memory).filter(Memory.user_id == user_id).all()

    if not memories:
        db.close()
        return []

    query_emb = get_embedding(expanded).reshape(1, -1)
    query_keywords = tokenize(query)

    is_broad = len(query_keywords) == 0   # key fix

    scored = []

    for mem in memories:
        emb = np.array(json.loads(mem.embedding)).reshape(1, -1)
        similarity = cosine_similarity(query_emb, emb)[0][0]

        # adaptive filtering
        if not is_broad and similarity < 0.3:
            continue

        importance = apply_decay(mem)
        now = datetime.now()

        if isinstance(mem.timestamp, str):
            ts = datetime.fromisoformat(mem.timestamp)
        elif isinstance(mem.timestamp, datetime):
            ts = mem.timestamp
        else:
            ts = now

        recency = 1 / (1 + (now - ts).days)

        mem_words = tokenize(mem.text)
        overlap = sum(1 for w in query_keywords if w in mem_words)

        keyword_score = overlap / len(query_keywords) if query_keywords else 0

        final_score = (
            0.7 * similarity +
            0.15 * importance +
            0.1 * recency +
            0.05 * keyword_score
        )

        scored.append((final_score, mem))

    scored.sort(reverse=True, key=lambda x: x[0])

    top_results = scored[:top_k]

    for _, mem in top_results:
        update_access(mem, db)

    results = [(score, mem.text) for score, mem in top_results]

    db.close()
    return results