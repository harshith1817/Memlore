# from src.memory_store import add_memory
# from src.retriever import retrieve
from src.database import engine, Base
from fastapi import FastAPI
from src.routes import router
from src import models

Base.metadata.create_all(bind=engine)


# # add_memory("I like machine learning")
# # add_memory("Deep learning is powerful")
# # add_memory("I enjoy playing cricket")


# def generate_answer(query):
#     results=retrieve(query)
    
#     if not results:
#         return "I don't have any memory about that yet."
    
#     context="\n".join(results)
    
#     response=f""" Based on your memory, here's what I found: {context}"""
    
#     return response


# while True:
#     user_input=input("You: ")
    
#     if user_input.lower().startswith("Store:"):
#         text=user_input.replace("store:", "").strip()
#         print(add_memory(text))
#     else:
#         print("AI:", generate_answer(user_input))



app=FastAPI()

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Memory AI Backend Running"}