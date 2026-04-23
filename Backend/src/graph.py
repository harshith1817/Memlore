import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

nlp = spacy.load("en_core_web_sm")
STOPWORDS = set(stopwords.words('english'))
graph = {}

def extract_entities(text):
    """SpaCy entity extraction + NLTK keyword fallback."""
    doc = nlp(text)
    entities = [ent.text.lower() for ent in doc.ents]
    
    # Also extract important nouns using SpaCy POS tagging
    nouns = [
        token.lemma_.lower() for token in doc
        if token.pos_ in ("NOUN", "PROPN")
        and token.text.lower() not in STOPWORDS
        and len(token.text) > 2
    ]
    
    # Combine — deduplicate
    all_concepts = list(set(entities + nouns))
    return all_concepts

def add_edge(a, b):
    if a not in graph:
        graph[a] = set()
    if b not in graph:
        graph[b] = set()
    graph[a].add(b)
    graph[b].add(a)

def build_graph(text):
    concepts = extract_entities(text)
    for i in range(len(concepts)):
        for j in range(i+1, len(concepts)):
            add_edge(concepts[i], concepts[j])

def expand_query(query):
    """Expand query with related concepts from graph."""
    concepts = extract_entities(query)
    related = []
    for c in concepts:
        if c in graph:
            related.extend(list(graph[c])[:3])  # limit to 3 related per concept
    expanded = query + " " + " ".join(set(related))
    return expanded.strip()