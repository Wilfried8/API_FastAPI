from typing import Optional
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends

from fastapi.params import Body
from pydantic import BaseModel

from random import randrange

import psycopg2
# import just the values of the columns without name
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

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

@app.get("/sqlal")
async def test_post(db: Session = Depends(get_db)):

    post = db.query(models.Posts).all()
    return {"status" : post }


@app.get("/posts")
async def get_post(db: Session = Depends(get_db)):
    # cursor.execute("""  
    #         SELECT * FROM posts
    # """)
    # posts = cursor.fetchall()
    posts = db.query(models.Posts).all()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post : Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """ insert into posts (title, content) values (%s, %s) RETURNING * """, (post.title, post.content)
    # )
    # post_p = cursor.fetchall()
    # conn.commit()
    create_post = models.Posts(title=post.title, content=post.content)
    db.add(create_post)
    db.commit()
    db.refresh(create_post)
    return {"data": create_post}

# read the last post : fait attention à la hierachie dans le code 
# @app.get("/posts/last_post")
# async def get_latest_post():
#     post_last = find_post(len(my_posts))
#     return {"detail": post_last}


@app.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """ SELECT * FROM posts WHERE id = %s RETURNING * """, (id,)
    # )
    # g_post_id = cursor.fetchone()

    get_post_by_id = db.query(models.Posts).filter(models.Posts.id == id).first()
    if get_post_by_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with the id : {id} was not found")
    return {"post_detail" : get_post_by_id}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s""", (id,)
    # )
    # conn.commit()
    del_post_by_id = db.query(models.Posts).filter(models.Posts.id == id).delete()
    db.commit()
    print(del_post_by_id)
    if del_post_by_id == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with the id : {id} doesn't exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """ UPDATE posts SET tittle = %s WHERE id = %s RETURNING *""", (post.title, id)
    # )
    # update_post = cursor.fetchone()
    # conn.commit()
    update_post_by_id = db.query(models.Posts).filter(models.Posts.id==id).first()
    print(update_post_by_id)
    if  update_post_by_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with the id : {id} doesn't exist")
    update_post_by_id.title = post.title
    update_post_by_id.content = post.content
    db.commit()
    return {"message" : update_post_by_id}

