from groq import Groq

client = Groq(api_key="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")

def generate_llm_response(query: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Answer concisely in 2-3 sentences. Never repeat yourself."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"GROQ ERROR: {e}")
        return f"Sorry, I couldn't process that right now."