from typing import Generator
from fastapi import FastAPI
from twilio.rest import Client as TwilioClient

from config import settings

from sqlalchemy.orm import Session

from server.database import SessionLocal, engine

from . import models, schema

twilio_client = TwilioClient(settings.twilio_account_sid, settings.twilio_auth_token)

message = twilio_client.messages.create(
    "+19517518340",
    from_="REDACTED",
    body="Hello from Python!")

print(message.sid)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
