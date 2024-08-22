from typing import Generator, Optional

from fastapi import Depends, FastAPI, UploadFile, Form, Response, Request
from twilio.twiml.messaging_response import MessagingResponse

from fastapi import Depends, FastAPI, UploadFile
from twilio.twiml.messaging_response import MessagingResponse

from fastapi import Depends, FastAPI, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
import crud

from sqlalchemy.orm import Session

from database import SessionLocal, engine, get_db
from sms import SmsClient
from database import engine, get_db

import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
twilio_client = SmsClient()


@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>Snapshot</title>
        </head>
        <body>
            <h1>Snapshot 📸</h1>
        </body>
    </html>
    """


@app.post("/upload/{user_hash}")
def upload(user_hash: str, file: UploadFile, db: Session = Depends(get_db)):
    user = crud.get_user_by_hash(db, user_hash)

    if user is None:
        raise HTTPException(status_code=400, detail="Invalid user")

    return crud.create_pic(db, user.username, file)


@app.post("/sms")
def receive_message(
    From: Optional[str] = Form(None),
    Body: Optional[str] = Form(None),
    MediaContentType0: Optional[str] = Form(None),
    MediaUrl0: Optional[str] = Form(None),
):
    if MediaContentType == "image":
        twilio.client.handle_image(From, MediaUrl0)
    else:
        twilio_client.handle_message(From, Body)
    response = MessagingResponse()
    return Response(content=str(response), media_type="application/xml")
