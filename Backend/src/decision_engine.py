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
THRESHOLD = 0.45
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

    if is_query(query):
        # Non-personal → straight to LLM
        # 1. Try DB first
        results = retrieve(user_id, query)

        if results:
            top_score, top_text = results[0]

            if top_score > THRESHOLD:
                return f"You told me that {format_memory_response(top_text)}"

        # Personal → check memory first
        results = retrieve(user_id, query)
        if results:
            good_results = [
                format_memory_response(text)
                for score, text in results
                if score > THRESHOLD
            ]
            if good_results:
                if len(good_results) == 1:
                    return f"Based on what you told me: {good_results[0]}"
                else:
                    combined = ", ".join(good_results)
                    return f"Based on what you told me: {combined}"
        return generate_llm_response(query)

    # Statement — split and store
    sentences = split_into_sentences(query)
    stored_count = 0
    for sentence in sentences:
        if is_meaningful(sentence):
            add_memory(user_id, sentence)
            stored_count += 1

    if stored_count > 0:
        return f"Got it! I've stored that."

    return generate_llm_response(query)