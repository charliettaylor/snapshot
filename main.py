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
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from twilio.twiml.messaging_response import MessagingResponse
from sqlalchemy.orm import Session

import crud
import models
from config import settings
from database import SessionLocal, engine, get_db
from sms import SmsClient
from database import engine, get_db

from constants import *

from datetime import datetime
from typing import Generator, Optional
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
twilio_client = SmsClient()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


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
    logger.info(
        "/sms %s %s %s %s", str(From), str(Body), str(MediaContentType0), str(MediaUrl0)
    )
    if MediaContentType0 is not None and "image" in MediaContentType0:
        twilio_client.handle_image(From, MediaUrl0)
    else:
        twilio_client.handle_message(From, Body)
    response = MessagingResponse()
    return Response(content=str(response), media_type="application/xml")


@app.get("/v/{user_hash}", response_class=HTMLResponse)
def images_page(
    user_hash: str,
    request: Request,
    n: Optional[int] = None,
    db: Session = Depends(get_db),
):
    prompt = crud.get_current_prompt(db)
    if n is None:
        n = prompt.id
    if not crud.get_submission_status(db, user_hash, n):
        raise HTTPException(status_code=401, detail="No submission for this prompt")

    pics = crud.get_pics_by_prompt(db, n)

    date_str = prompt.date.strftime("%b %-d, %Y")

    return templates.TemplateResponse(
        request=request, name="gallery.html", context={"pics": pics, "prompt": prompt.prompt, "date": date_str}
    )


@app.get("/v/{user_hash}/history", response_class=HTMLResponse)
def history_page(user_hash: str, db: Session = Depends(get_db)):
    pics = crud.get_pics_by_hash(db, user_hash)
    html_list = []
    for pic in pics:
        prompt = crud.get_prompt(db, pic.prompt)
        url = BASE_URL + "{}?n={}".format(user_hash, prompt.id)
        html_list.append('<li><a href="{}">{}</a></li>'.format(url, prompt.prompt))

    return """
    <html>
        <head>
            <title>Snapshot</title>
        </head>
        <body>
            <h1>History</h1>
            <ul>{}</ul>
        </body>
    </html>
    """.format(
        "".join(html_list)
    )
