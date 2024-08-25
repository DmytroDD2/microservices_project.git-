from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas, models
from .db.session import get_db
from .services.rabbitmq_service import start_worker, rb_send
import threading
router = APIRouter()



@router.post("", tags=["user_service"], status_code=201)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user=user)
    massage = {
        'recipient': db_user.email,
        'subject': 'Registration was successful',
        'body': 'You have successfully registered'
    }

    threading.Thread(target=start_worker).start()
    rb_send(massage)

    return db_user


@router.get("/{user_id}", tags=["user_service"], status_code=200)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get('/users/', status_code=200)
async def read_users(db: Session = Depends(get_db)):
    db_users = crud.get_all(db=db)
    return db_users


@router.put("/{user_id}", tags=["user_service"], status_code=200)
async def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}", tags=["user_service"], status_code=204)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db=db, user_id=user_id)
