from typing import List
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from .. import models, schema, utils, oauth2
from ..database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# @router.get("/")
# async def root():
#     return {"message": "welcome wil"}

# @app.get("/sqlal")
# async def test_post(db: Session = Depends(get_db)):

#     post = db.query(models.Posts)
#     print(post)
#     return {"status" : post.all() }


@router.get("/", response_model=List[schema.Post])
async def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#async def get_post(db: Session = Depends(get_db)):
    # cursor.execute("""  
    #         SELECT * FROM posts
    # """)
    # posts = cursor.fetchall()
    posts = db.query(models.Posts).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
async def create_posts(post : schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#async def create_posts(post : schema.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute(
    #     """ insert into posts (title, content) values (%s, %s) RETURNING * """, (post.title, post.content)
    # )
    # post_p = cursor.fetchall()
    # conn.commit()
    #print(**post.dict())
    print(f" the id of the user is : {current_user.id} and his email is : {current_user.email}")
    create_post = models.Posts(**post.dict())
    db.add(create_post)
    db.commit()
    db.refresh(create_post)
    return create_post

@router.get("/{id}", response_model=schema.Post)
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#async def get_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute(
    #     """ SELECT * FROM posts WHERE id = %s RETURNING * """, (id,)
    # )
    # g_post_id = cursor.fetchone()

    get_post_by_id = db.query(models.Posts).filter(models.Posts.id == id).first()
    
    if get_post_by_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with the id : {id} was not found")
    return get_post_by_id


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#async def delete_post(id: int, db: Session = Depends(get_db)):

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


@router.put("/{id}", response_model=schema.Post)
async def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#async def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db)):

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