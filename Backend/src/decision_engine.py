from src.retriever import retrieve
from src.llm import generate_llm_response
from src.memory_store import add_memory

Threshold=0.4


def is_memory(text):
    text = text.lower().strip()

    if text.endswith("?"):
        return False

    question_words = ["what", "who", "where", "when", "why", "how"]
    if any(text.startswith(q) for q in question_words):
        return False

    memory_patterns = [
        "i am", "my name is", "i like", "i love", "i enjoy"
    ]

    return any(p in text for p in memory_patterns)


def split_query(text):
    text = text.lower()
    separators = [" and ", " but ", " also ", ".", "?"]
    parts = [text]
    for sep in separators:
        temp = []
        for p in parts:
            temp.extend(p.split(sep))
        parts = temp
    return [p.strip() for p in parts if p.strip()]


def is_query(text):
    question_words = ["what", "who", "where", "when", "why", "how"]
    return any(text.startswith(q) for q in question_words)


def is_incomplete(text):
    text = text.strip().lower()

    # ends with incomplete patterns
    incomplete_patterns = [
        "is",
        "are",
        "am",
        "my",
        "i like",
        "i love",
        "i enjoy"
    ]

    # if sentence is too short
    if len(text.split()) < 3:
        return True

    # ends with incomplete phrase
    if any(text.endswith(p) for p in incomplete_patterns):
        return True

    return False



def answer(query, user_id):
    
    if is_memory(query):
        add_memory(user_id, query)
        return "Got it! I've stored that in memory."
        
    results=retrieve(user_id, query)
    
    if results:
        top_score, _=results[0]
        
        if top_score>Threshold:
            context="\n".join([text for _, text in results])
            return f"Based on your memory:\n{context}"
        
        # if top_score > Threshold:
        #     context = results[0][1]   # only best memory
        #     return f"You told me that {context}"

    return generate_llm_response(query)