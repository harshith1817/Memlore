from src.database import engine, Base
from fastapi import FastAPI
from src.routes import router
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Memory AI Backend Running"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key"
)