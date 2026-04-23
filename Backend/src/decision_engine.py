from src.retriever import retrieve
from src.llm import generate_llm_response
from src.memory_store import add_memory

Threshold=0.5


def is_memory(text):
    text = text.lower().strip()

    if is_query(text):
        return False

    if is_incomplete(text):
        return False

    words = text.split()

    if len(words) < 3:
        return False

    junk = ["ok", "okay", "yes", "no", "hmm", "lol", "nice"]
    if text in junk:
        return False
    return True


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
    if len(text.split()) < 2:
        return True
    return False



def answer(query, user_id):

    if is_incomplete(query):
        return "Can you complete that?"

    parts = split_query(query)

    stored = False
    query_parts = []

    for part in parts:
        if is_memory(part):
            add_memory(user_id, part)
            stored = True
        elif is_query(part):
            query_parts.append(part)

    if query_parts:
        q = " ".join(query_parts)

        results = retrieve(user_id, q)

        if results:
            top_score, _ = results[0]

            if top_score > Threshold:
                return f"You told me that {results[0][1]}"

        return generate_llm_response(q)

    if stored:
        return "Got it! I've stored that in memory."

    return generate_llm_response(query)