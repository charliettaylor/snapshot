from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    UploadFile,
    Form,
    Response,
    Request,
    Body,
)
from fastapi.responses import HTMLResponse
from twilio.twiml.messaging_response import MessagingResponse
from sqlalchemy.orm import Session

import crud
import models
from config import settings
from database import SessionLocal, engine, get_db
from sms import SmsClient
from database import engine, get_db

from typing import Generator, Optional

models.Base.metadata.create_all(bind=engine)

prompt_num = None

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


@app.post("/u/{user_hash}")
def upload(user_hash: str, file: UploadFile, db: Session = Depends(get_db)):
    user = crud.get_user_by_hash(db, user_hash)

    if user is None:
        raise HTTPException(status_code=400, detail="Invalid user")

    pic = crud.create_pic(db, user.username, file)
    if pic is None:
        raise HTTPException(status_code=400, detail="Already submitted pic")

    return pic


@app.post("/sms")
def receive_message(
    From: Optional[str] = Form(None),
    Body: Optional[str] = Form(None),
    MediaContentType0: Optional[str] = Form(None),
    MediaUrl0: Optional[str] = Form(None),
):
    if MediaContentType0 == "image":
        twilio.client.handle_image(From, MediaUrl0)
    else:
        twilio_client.handle_message(From, Body)
    response = MessagingResponse()
    return Response(content=str(response), media_type="application/xml")


@app.get("/{user_hash}")
def images_page(user_hash: str, n: Optional[int]):
    if n is None:
        n = crud.get_current_prompt().id
    if not crud.get_submission_status(user_hash, n):
        return HTTPException(status_code=401, detail="No submission for this prompt")
    return """
    <html>
        <head>
            <title>Snapshot</title>
        </head>
        <body>
            <h1>You submitted a snapshot! 📸</h1>
        </body>
    </html>
    """


@app.get("/{user_hash}/history")
def history_page(user_hash: str):
    pass
