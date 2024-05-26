from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from .. import models, schema, utils, oauth2
from ..database import engine, get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentification"]
)

@router.post("/login", response_model=schema.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # OAuth2PasswordRequestForm return : Username and password
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= f"Invalid credential")
    
    if not utils.verify_password(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= f"Invalid credential")
    
    #create token
    # return token
    access_token = oauth2.create_access_token(
        data={
            "user_id":user.id
        }
    )

    return {"access_token" : access_token, "token_type":"Bearer"}