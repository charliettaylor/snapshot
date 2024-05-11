from typing import Generator
from fastapi import Depends, FastAPI, UploadFile

from config import settings
import crud

from sqlalchemy.orm import Session

from database import SessionLocal, engine, get_db

import schema, models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    user = None
    if isinstance(db, Session):
        user = db.query(schema.User).first()

    return user

@app.post('/upload/{user_hash}')
def upload(user_hash: str, file: UploadFile, db: Session = Depends(get_db)):
    user = crud.get_user_by_hash(db, user_hash)

    if user is None:
        return None

    return crud.create_pic(db, user.username, file)