from typing import Optional, List
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends

from fastapi.params import Body
from pydantic import BaseModel

from random import randrange

import psycopg2
# import just the values of the columns without name
from psycopg2.extras import RealDictCursor
import time
from . import models, schema
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

# @app.get("/sqlal")
# async def test_post(db: Session = Depends(get_db)):

#     post = db.query(models.Posts)
#     print(post)
#     return {"status" : post.all() }


@app.get("/posts", response_model=List[schema.Post])
async def get_post(db: Session = Depends(get_db)):
    # cursor.execute("""  
    #         SELECT * FROM posts
    # """)
    # posts = cursor.fetchall()
    posts = db.query(models.Posts).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
async def create_posts(post : schema.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """ insert into posts (title, content) values (%s, %s) RETURNING * """, (post.title, post.content)
    # )
    # post_p = cursor.fetchall()
    # conn.commit()
    #print(**post.dict())
    create_post = models.Posts(**post.dict())
    db.add(create_post)
    db.commit()
    db.refresh(create_post)
    return create_post

@app.get("/posts/{id}", response_model=schema.Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """ SELECT * FROM posts WHERE id = %s RETURNING * """, (id,)
    # )
    # g_post_id = cursor.fetchone()

    get_post_by_id = db.query(models.Posts).filter(models.Posts.id == id).first()
    
    if get_post_by_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with the id : {id} was not found")
    return get_post_by_id


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s""", (id,)
    # )
    # conn.commit()
    del_post_by_id = db.query(models.Posts).filter(models.Posts.id == id)
    if del_post_by_id.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with the id : {id} doesn't exist")
    del_post_by_id.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schema.Post)
async def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """ UPDATE posts SET tittle = %s WHERE id = %s RETURNING *""", (post.title, id)
    # )
    # update_post = cursor.fetchone()
    # conn.commit()
    update_post_by_id = db.query(models.Posts).filter(models.Posts.id==id)
    print(update_post_by_id)
    if  update_post_by_id.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with the id : {id} doesn't exist")
    # update_post_by_id.title = post.title
    # update_post_by_id.content = post.content
    update_post_by_id.update(post.dict(), synchronize_session=False)

    db.commit()
    return update_post_by_id.first()


@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    create_user = models.Users(**user.dict())
    db.add(create_user)
    db.commit()
    db.refresh(create_user)
    return create_user