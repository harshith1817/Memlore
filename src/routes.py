from fastapi import APIRouter
from src.memory_store import add_memory
from src.decision_engine import answer

router=APIRouter()

@router.post("/add-memory")
def add_memory_api(text: str):
    add_memory(text)
    return {"status": "stored"}

@router.get("/query")
def query_api(q: str):
    results=answer(q)
    return {"response": results}