from typing import Generator
from fastapi import FastAPI

from config import settings

from sqlalchemy.orm import Session

from database import SessionLocal, engine, get_db

import models
import schema

app = FastAPI()

@app.get("/")
def read_root():
    db = get_db()
    user = None
    if isinstance(db, Session):
        user = db.query(models.User).first()

    return user

@app.get("/test")
def test():
    db = get_db()
    us = models.User(username="test", phone="123-456-7890", is_active=True)
    if isinstance(db, Session):
        db.add(us)
        db.commit()
        db.refresh(us)

    return us
