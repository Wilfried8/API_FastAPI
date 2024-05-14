from typing import Optional
from fastapi import FastAPI, Body

from fastapi.params import Body
from pydantic import BaseModel

from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite food", "content": "i like pizza", "id": 2}
            ]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


@app.get("/")
async def root():
    return {"message": "welcome wil"}


@app.get("/posts")
async def get_post():
    return {"data": my_posts}


@app.post("/posts")
async def create_posts(post : Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)

    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
async def get_post(id: int):
    post_id = find_post(id)
    print(type(id))
    return {"post_detail" : post_id}


