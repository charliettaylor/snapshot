from typing import Generator
from fastapi import Depends, FastAPI

from config import settings

from sqlalchemy.orm import Session

from database import SessionLocal, engine, get_db

import schema, models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    db = get_db()
    user = None
    if isinstance(db, Session):
        user = db.query(schema.User).first()

    return user
