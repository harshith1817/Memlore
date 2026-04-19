from fastapi import APIRouter
from src.memory_store import add_memory
from src.retriever import retrieve

router=APIRouter()

@router.post("/add-memory")
def add_memory_api(text: str):
    add_memory(text)
    return {"status": "stored"}

@router.get("/query")
def query_api(q: str):
    results=retrieve(q)
    return {"response": results}