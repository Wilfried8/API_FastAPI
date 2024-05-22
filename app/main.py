
from fastapi import FastAPI
from . import models
from .database import engine

from passlib.context import CryptContext

from .routers import post, user, auth

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "welcome wil"}