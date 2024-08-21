from typing import Generator

from fastapi import Depends, FastAPI, UploadFile, Form
from twilio.twiml.messaging_response import MessagingResponse

from config import settings
import crud

from sqlalchemy.orm import Session

from database import SessionLocal, engine, get_db
from sms import SmsClient

import schema, models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
twilio_client = SmsClient()

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

@app.post("/sms")
def receive_message(from_: str = Form(...), body: str = Form(...)):
    twilio_client.receive_message(from_, body)
    twilio_client.send_message(from_, "Received message {}".format(body))
