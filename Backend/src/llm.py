from transformers import pipeline

llm=pipeline("text-generation", model="gpt2")

def generate_llm_response(prompt):
    response=llm(prompt, max_length=100)[0]['generated_text']
    return response