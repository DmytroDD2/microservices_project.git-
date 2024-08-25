from fastapi import APIRouter, Depends, HTTPException
from pydantic import json
from sqlalchemy.orm import Session
from . import crud, schemas
from .db.session import get_db
import httpx


router = APIRouter()


async def fetch_user(user_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://user-service:8000/user_service/{user_id}")
        response.raise_for_status()
        return response.json()


@router.post("/posts/", response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    try:
        await fetch_user(post.user_id)
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.create_post(db=db, post=post)


@router.get("/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db=db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.get("/posts/", response_model=list[schemas.Post])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_posts(db=db, skip=skip, limit=limit)


@router.delete("/posts/{post_id}", response_model=schemas.Post)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db=db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.delete_post(db=db, post_id=post_id)
