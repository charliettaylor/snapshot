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
from util import super_duper_good_hash
from database import SessionLocal, engine, get_db
from sms import SmsClient
from database import engine, get_db

from typing import Generator, Optional

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

@app.post('/u/{user_hash}')
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
    if MediaContentType == "image":
        twilio.client.handle_image(From, MediaUrl0)
    else:
        twilio_client.handle_message(From, Body)
    response = MessagingResponse()
    return Response(content=str(response), media_type="application/xml")


@app.post("/send_prompt")
def send_prompt(prompt: str = Body(...), password: str = Body(...)):

    ### insert prompt into db

    if super_duper_good_hash(password) != settings.admin_hash:
        return HTTPException(status_code=401, detail="Wrong password, LOSER!")
    twilio_client.send_prompts(prompt)
