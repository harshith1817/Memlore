from fastapi import APIRouter, Header, Depends
from src.memory_store import add_memory
from src.decision_engine import answer
from src.auth import hash_password, verify_password, create_token, decode_token
from src.models import User
from src.database import SessionLocal

router=APIRouter()

@router.post("/signup")
def signup(email: str, password: str):
    db=SessionLocal()
    user=User(
        email=email,
        password=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.close()
    return {"status": "User created"}


@router.post("/login")
def login(email: str, password: str):
    db=SessionLocal()
    user=db.query(User).filter(User.email==email).first()
    if not user or not verify_password(password, user.password):
        return {"error": "Invalid credentials"}
    token=create_token({"user_id": user.id})
    return {"access_token": token}


def get_current_user(token: str=Header(...)):
    payload=decode_token(token)
    return payload["user_id"]
    

@router.post("/add-memory")
def add_memory_api(text: str, user_id: int=Depends(get_current_user)):
    add_memory(user_id, text)
    return {"status": "stored"}

@router.get("/query")
def query_api(q: str, user_id: int=Depends(get_current_user)):
    results=answer(q, user_id)
    return {"response": results}