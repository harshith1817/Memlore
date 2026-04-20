from src.retriever import retrieve
from src.llm import generate_llm_response

Threshold=0.4

def answer(query, user_id):
    results=retrieve(user_id, query)
    
    if not results:
        return generate_llm_response(query)
    
    top_score, _=results[0]
    
    if top_score>Threshold:
        context="\n".join([text for _, text in results])
        return f"Based on your memory:\n{context}"
    else:
        return generate_llm_response(query)