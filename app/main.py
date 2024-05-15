from typing import Optional
from fastapi import FastAPI, Body, Response, status, HTTPException

from fastapi.params import Body
from pydantic import BaseModel

from random import randrange

import psycopg2
# import just the values of the columns without name
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True :
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was succesfull !!!')
        break
    except Exception as e:
        print('connection to DB failed')
        print('Error', f'e')
        time.sleep(2)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite food", "content": "i like pizza", "id": 2}
            ]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        #print(i, p)
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "welcome wil"}


@app.get("/posts")
async def get_post():
    cursor.execute("""  
            SELECT * FROM posts
    """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# async def create_posts(post : Post):
#     post_dict = post.dict()
#     post_dict['id'] = randrange(0, 100000)

#     my_posts.append(post_dict)
#     return {"data": post_dict}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post : Post):
    cursor.execute(
        """ insert into posts (tittle, content) values (%s, %s) RETURNING * """, (post.title, post.content)
    )
    post_p = cursor.fetchall()
    return {"data": post_p}

# read the last post : fait attention à la hierachie dans le code 
# @app.get("/posts/last_post")
# async def get_latest_post():
#     post_last = find_post(len(my_posts))
#     return {"detail": post_last}


@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    post = find_post(id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with the id : {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': f"post with the id : {id} was not found"}
    return {"post_detail" : post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    # deleting post
    # find the index in the array that has required ID
    # my_post.pop(index)
    index = find_index_post(id)
    if index == None:
        print("delete")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with the id : {id} doesn't exist")
    my_posts.pop(index)
    #return {"message": "post was successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    print(post)
    index = find_index_post(id)
    if index == None:
        print("delete")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with the id : {id} doesn't exist")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    print(post_dict)
    return {"message" : post_dict}


