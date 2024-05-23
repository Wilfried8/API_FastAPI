from typing import List, Optional
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from .. import models, schema, utils, oauth2
from ..database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/votes",
    tags=["votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_vote(vote: schema.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.users_id == current_user.id)
    found_votes = vote_query.first()
    if (vote.dir == 1):
        if found_votes:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail= f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Votes(post_id = vote.post_id, users_id=current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "successfully added vote"}
    
    else:
        if not found_votes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        
        return {"message":"successfully deletes vote"}
    
    