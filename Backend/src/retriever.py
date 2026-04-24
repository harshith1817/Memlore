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

nlp = spacy.load("en_core_web_sm")
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

STOPWORDS = set(stopwords.words('english'))

def apply_decay(memory):
    last = datetime.fromisoformat(memory.last_accessed)
    now = datetime.now()
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
    
    
def retrieve(user_id, query, top_k=2):
    expanded = expand_query(query)
    db = SessionLocal()
    memories = db.query(Memory).filter(Memory.user_id == user_id).all()

    query_emb = get_embedding(expanded).reshape(1, -1)
    scored = []

    for mem in memories:
        emb = np.array(json.loads(mem.embedding)).reshape(1, -1)
        similarity = cosine_similarity(query_emb, emb)[0][0]
        importance = apply_decay(mem)
        recency = 1 / (1 + (datetime.now() - datetime.fromisoformat(mem.timestamp)).days)

        # NLTK keyword matching
        keyword_score = 0
        query_keywords = tokenize(query)
        mem_words = tokenize(mem.text)
        for word in query_keywords:
            if word in mem_words:
                keyword_score += 1
        if len(query_keywords) > 0:
            keyword_score = keyword_score / len(query_keywords)

        final_score = (
            0.5 * similarity +
            0.25 * importance +
            0.1 * recency +
            0.25 * keyword_score
        )

        scored.append((final_score, mem))

    scored.sort(reverse=True, key=lambda x: x[0])
    filtered = [(score, mem) for score, mem in scored if score > 0.45]

    if not filtered:
        db.close()
        return []

    top_results = filtered[:top_k]

    for _, mem in top_results:
        update_access(mem, db)

    results = [(score, mem.text) for score, mem in top_results]
    db.close()
    return results