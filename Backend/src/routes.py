from fastapi import APIRouter, Header, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from src.memory_store import add_memory
from src.decision_engine import answer
from src.auth import hash_password, verify_password, create_token, decode_token
from src.oauth import oauth
from src.models import User, Memory
from src.database import SessionLocal
from pydantic import BaseModel, EmailStr

router=APIRouter()
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    
@router.post("/signup")
def signup(data: SignupRequest):
    db = SessionLocal()
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="User already exists")
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
        raise HTTPException(status_code=404, detail="User not found!")

    if user.password is None:
        user.password = hash_password(data.password)
        db.commit()

        token = create_token({"user_id": user.id})
        db.close()
        return {"access_token": token}

    if not verify_password(data.password, user.password):
        db.close()
        raise HTTPException(status_code=401, detail="Enter a valid password")

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


@router.get("/auth/google")
async def google_login(request: Request):
    redirect_uri = "http://localhost:8000/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/google/callback")
async def google_callback(request: Request):
    db = SessionLocal()

    token = await oauth.google.authorize_access_token(request)

    resp = await oauth.google.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        token=token
    )

    user_info = resp.json()
    email = user_info.get("email")

    if not email:
        db.close()
        raise HTTPException(status_code=400, detail="Email not found")

    # check if user exists
    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(
            id=email,
            email=email,
            password=None
        )
        db.add(user)
        db.commit()

    jwt_token = create_token({"user_id": user.id})

    db.close()

    return RedirectResponse(
        url=f"http://localhost:3000/oauth-success?token={jwt_token}"
    )
    

@router.get("/auth/github")
async def github_login(request: Request):
    redirect_uri = "http://localhost:8000/auth/github/callback"
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get("/auth/github/callback")
async def github_callback(request: Request):
    db = SessionLocal()

    token = await oauth.github.authorize_access_token(request)

    resp = await oauth.github.get("user", token=token)
    user_info = resp.json()

    email = user_info.get("email")

    if not email:
        emails_resp = await oauth.github.get("user/emails", token=token)
        emails = emails_resp.json()
        email = next((e["email"] for e in emails if e["primary"]), None)

    if not email:
        db.close()
        raise HTTPException(status_code=400, detail="Email not found")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(
            id=email,
            email=email,
            password=None
        )
        db.add(user)
        db.commit()

    jwt_token = create_token({"user_id": user.id})

    db.close()

    return RedirectResponse(
        url=f"http://localhost:3000/oauth-success?token={jwt_token}"
    )
    

@router.delete("/clear-memory")
def clear_memory(user_id: str = Depends(get_current_user)):
    db = SessionLocal()

    deleted=db.query(Memory).filter(Memory.user_id == user_id).delete()

    db.commit()
    db.close()

    return {"status": "cleared", "deleted": deleted}