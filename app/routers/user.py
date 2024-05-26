from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from .. import models, schema, utils
from ..database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    
    # hash the password - user.password
    #hashed_password = pwd_context.hash(user.password)
    user.password = utils.hash(user.password)

    create_user = models.Users(**user.dict())
    db.add(create_user)
    db.commit()
    db.refresh(create_user)
    return create_user

@router.get("/{id}", response_model=schema.UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    
    get_user_by_id = db.query(models.Users).filter(models.Users.id == id).first()
    
    if get_user_by_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"user with the id : {id} doesn't exist")
    return get_user_by_id