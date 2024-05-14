from typing import Optional
from fastapi import FastAPI, Body

from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "welcome wil"}


@app.get("/posts")
async def get_post():
    return {"data": "this is your post deux bis"}


@app.post("/create_posts")
async def create_posts(post : Post):
    print(post.dict())
    return {"data": post}

# title str, content str, category,  
