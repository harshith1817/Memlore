from fastapi import APIRouter, Header, Depends, HTTPException
from src.memory_store import add_memory
from src.decision_engine import answer
from src.auth import hash_password, verify_password, create_token, decode_token
from src.models import User
from src.database import SessionLocal
from pydantic import BaseModel

router=APIRouter()
class SignupRequest(BaseModel):
    email: str
    password: str
    
@router.post("/signup")
def signup(data: SignupRequest):
    db = SessionLocal()
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        db.close()
        return {"error": "User already exists"}
    user = User(
        id=data.email,
        email=data.email,
        password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.close()
    return {"status": "User created"}


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(data.password, user.password):
        db.close()
        raise HTTPException(status_code=401, detail="Wrong password")
    token = create_token({"user_id": user.id})
    db.close()
    return {"access_token": token}


def get_current_user(token: str=Header(...)):
    payload=decode_token(token)
    return payload["user_id"]
    

@router.post("/add-memory")
def add_memory_api(text: str, user_id: str = Depends(get_current_user)):
    add_memory(user_id, text)
    return {"status": "stored"}

@router.get("/query")
def query_api(q: str, user_id: str = Depends(get_current_user)):
    results=answer(q, user_id)
    return {"response": results}