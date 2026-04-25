import re
import random
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from rapidfuzz import fuzz
from src.retriever import retrieve
from src.llm import generate_llm_response
from src.memory_store import add_memory
import spacy
nlp = spacy.load("en_core_web_sm")

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

STOPWORDS = set(stopwords.words('english'))
THRESHOLD = 0.55
QUESTION_WORDS = []
PERSONAL_WORDS = {"my", "i", "me", "mine", "our"}

GREETINGS = {
    "hi", "hey", "hello", "hola", "howdy", "sup", "what's up",
    "whats up", "yo", "greetings", "good morning", "good afternoon",
    "good evening"
}

FAREWELLS = {
    "bye", "goodbye", "see you", "see ya", "cya", "later",
    "take care", "farewell", "good night", "gn", "ttyl"
}

GREETING_RESPONSES = [
    "Hey! How can I help you today?",
    "Hello! Tell me something or ask me anything.",
    "Hi there! What's on your mind?",
    "Hey! I'm here. What do you want to know or share?",
]

FAREWELL_RESPONSES = [
    "Bye! Take care!",
    "See you later! I'll remember everything you told me.",
    "Goodbye! Come back anytime.",
    "Take care! Your memories are safe with me.",
]

    
def get_intent(text):
    text = text.strip().lower().rstrip("?!.")
    if text in GREETINGS:
        return "greeting"
    if text in FAREWELLS:
        return "farewell"
    # Fuzzy match for close greetings like "heyy", "helloo"
    for g in GREETINGS:
        if fuzz.ratio(text, g) > 85:
            return "greeting"
    for f in FAREWELLS:
        if fuzz.ratio(text, f) > 85:
            return "farewell"
    return None

def is_query(text):
    text = text.lower().strip()
    words = text.split()

    if not words:
        return False

    # 1. Question mark
    if text.endswith("?"):
        return True

    # 2. WH words
    wh_words = ["what", "who", "where", "when", "why", "how", "which", "whose"]
    if words[0] in wh_words:
        return True

    # 3. Auxiliary verbs
    aux_verbs = [
        "do", "does", "did",
        "is", "am", "are",
        "was", "were",
        "can", "could",
        "will", "would",
        "have", "has", "had"
    ]
    if words[0] in aux_verbs:
        return True

    # 4. Command-style queries
    command_words = ["tell", "give", "show", "list", "find", "get"]
    if words[0] in command_words:
        return True

    return False

def is_personal_query(text):
    words = text.lower().split()
    if any(w in PERSONAL_WORDS for w in words):
        return True
    # "what is X" — always check memory first
    if text.lower().startswith("what is"):
        return True
    return False

def is_incomplete(text):
    return len(text.strip().split()) < 2

def is_meaningful(text):
    """Check if a sentence is worth storing."""
    text = text.strip()
    if not text:
        return False
    tokens = word_tokenize(text.lower())
    meaningful = [w for w in tokens if w.isalpha() and w not in STOPWORDS]
    if len(meaningful) < 2:
        return False
    if get_intent(text):
        return False
    if is_query(text):
        return False
    return True

def split_into_sentences(text):
    """
    Smart splitting using NLTK + pattern detection.
    Handles text without punctuation.
    """
    # First try NLTK sent_tokenize
    sentences = sent_tokenize(text)
    
    result = []
    for sentence in sentences:
        # Split on conjunctions
        parts = re.split(r'\band\b|\bbut\b|\balso\b', sentence, flags=re.IGNORECASE)
        for part in parts:
            # Further split on "I + verb" pattern for unpunctuated text
            # "My name is Harsh I am 23" → ["My name is Harsh", "I am 23"]
            sub_parts = re.split(r'(?<!\w)\s+(?=I\s+(?:am|work|live|love|like|enjoy|have|do|study|use|play|watch))', part, flags=re.IGNORECASE)
            result.extend(sub_parts)
    
    cleaned = [s.strip().lower() for s in result if s.strip()]
    return cleaned

def format_memory_response(text):
    doc = nlp(text)
    tokens = []
    
    text = text.strip()

    if not text.startswith("you"):
        text = "you " + text

    text = text[0].upper() + text[1:]

    if not text.endswith("."):
        text += "."
        
    for token in doc:
        word = token.text.lower()
        if word == "i" and token.pos_ == "PRON":
            tokens.append("you")
        elif word == "my" and token.pos_ == "PRON":
            tokens.append("your")
        elif word == "me" and token.pos_ == "PRON":
            tokens.append("you")
        elif word == "mine" and token.pos_ == "PRON":
            tokens.append("yours")
        elif word == "am" and token.pos_ == "AUX":
            tokens.append("are")
        else:
            tokens.append(word)
    
    result = " ".join(tokens)
    
    # Tiny fallback for common SpaCy misses
    result = result.replace(" i ", " you ").replace(" my ", " your ")
    return result.strip().capitalize()


def is_broad_query(query):
    query = query.lower()

    intent_words = {"tell", "know", "describe", "summarize", "list", "show"}
    personal_words = {"me", "my", "myself", "mine"}

    tokens = query.split()

    has_intent = any(w in tokens for w in intent_words)
    has_personal = any(w in tokens for w in personal_words)

    return has_intent and has_personal

def answer(query, user_id):
    query = query.strip()

    # Handle greetings and farewells
    intent = get_intent(query)
    if intent == "greeting":
        return random.choice(GREETING_RESPONSES)
    if intent == "farewell":
        return random.choice(FAREWELL_RESPONSES)

    if is_incomplete(query):
        return "Can you tell me more?"
    
    if " and " in query and is_query(query):
        parts = query.split(" and ")
        responses = []

        for part in parts:
            res = answer(part.strip(), user_id)
            responses.append(res)

        return " ".join(responses)
    

    if is_query(query):

        if is_broad_query(query):
            results = retrieve(user_id, query, top_k=5)
    
            # fallback: if retriever still fails → fetch raw memory
            if not results:
                from src.database import SessionLocal
                from src.models import Memory

                db = SessionLocal()
                memories = db.query(Memory).filter(Memory.user_id == user_id).all()
                db.close()

                if not memories:
                    return generate_llm_response(query)

                # take last few memories
                results = [(1.0, mem.text) for mem in memories[-5:]]

            responses = [
                format_memory_response(text)
                for _, text in results
            ]

            return "Here's what I know: " + ", ".join(responses)
        
        results = retrieve(user_id, query)
        
        if not results:
            return generate_llm_response(query)

        top_score = results[0][0]

        # Dynamic gap
        gap = 0.1 if top_score > 0.7 else 0.05

        filtered = [
            (score, text)
            for score, text in results
            if score >= top_score - gap
        ]

        good_results = [
            format_memory_response(text)
            for score, text in filtered
        ]

        # No strong match → fallback or best guess
        if not good_results:
            if top_score < 0.45:
                return generate_llm_response(query)

            return f"You told me that {format_memory_response(results[0][1])}"

        if len(good_results) == 1:
            return f"You told me that {good_results[0]}"

        return "Based on what you told me: " + ", ".join(good_results)

    # Statement — split and store
    sentences = split_into_sentences(query)
    stored_count = 0
    for sentence in sentences:
        if is_meaningful(sentence):
            add_memory(user_id, sentence)
            stored_count += 1

    if stored_count > 0:
        return f"Got it! I've stored everything you told me."

    return generate_llm_response(query)