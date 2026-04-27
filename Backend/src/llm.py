from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing")

client = Groq(api_key=api_key)

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