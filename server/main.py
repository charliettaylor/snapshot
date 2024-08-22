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


@app.post("/sms")
def receive_message(
    From: Optional[str] = Form(None),
    Body: Optional[str] = Form(None),
    MediaContentType0: Optional[str] = Form(None),
    MediaUrl0: Optional[str] = Form(None),
):
    print(From, Body, MediaContentType0, MediaUrl0)
    if MediaContentType0 is not None and "image" in MediaContentType0:
        twilio_client.handle_image(From, MediaUrl0)
    else:
        twilio_client.handle_message(From, Body)
    response = MessagingResponse()
    return Response(content=str(response), media_type="application/xml")


@app.get("/{user_hash}")
def images_page(user_hash: str, n: Optional[int] = None, db: Session = Depends(get_db)):
    if n is None:
        n = crud.get_current_prompt(db).id
    if not crud.get_submission_status(db, user_hash, n):
        return HTTPException(status_code=401, detail="No submission for this prompt")

    pics = crud.get_pics_by_prompt(db, n)
    html_list = []
    for pic in pics:
        html_list.append('<li><img src="{}"></li>'.format(pic.url))

    return """
    <html>
        <head>
            <title>Snapshot</title>
        </head>
        <body>
            <h1>Submissions</h1>
            <ul>
            {}
            </ul>
        </body>
    </html>
    """.format(
        "".join(html_list)
    )


@app.get("/{user_hash}/history")
def history_page(user_hash: str, db: Session = Depends(get_db)):
    pics = crud.get_pics_by_hash(db, user_hash)
    html_list = []
    for pic in pics:
        html_list.append("<li>{}/li>".format(pic.id))

    return """
    <html>
        <head>
            <title>Snapshot</title>
        </head>
        <body>
            <h1>History</h1>
            <ul>
                {}
            </ul>
        </body>
    </html>
    """.format(
        "".join(html_list)
    )
