import logging
from typing import Optional

from fastapi import Depends, FastAPI, Form, HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from twilio.twiml.messaging_response import MessagingResponse

import crud
import models
from constants import *
from database import engine, get_db
from sms import SmsClient

logging.basicConfig(
    level=logging.INFO,
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
    prompt = None
    if n is not None:
        prompt = crud.get_prompt(db, n)
    else:
        prompt = crud.get_current_prompt(db)
        n = prompt.id

    if not crud.get_submission_status(db, user_hash, n):
        raise HTTPException(status_code=401, detail="No submission for this prompt")

    pics = crud.get_pics_by_prompt(db, n)

    date_str = prompt.date.strftime("%b %-d, %Y")

    return templates.TemplateResponse(
        request=request,
        name="gallery.html",
        context={"pics": pics, "prompt": prompt.prompt, "date": date_str},
    )


@app.get("/h/{user_hash}", response_class=HTMLResponse)
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
