from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from .. import models, schema, utils
from ..database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Authentification"]
)

@router.post("/login")
async def login(user_credentials: schema.UserLogin, db: Session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Invalid credential")
    
    if not utils.verify_password(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Invalid credential")
    
    #create token
    # return token

    return {"token" : "dghgfhrhr"}