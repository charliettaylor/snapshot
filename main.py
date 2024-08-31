import logging
from typing import Optional

from fastapi import Depends, FastAPI, Form, HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from SmsClient import SmsClient
from sqlalchemy.orm import Session
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

import models
from config import settings
from constants import *
from database import Database, engine

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
twilio_client = SmsClient(settings)
templates = Jinja2Templates(directory="templates")
db = Database()

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
async def receive_message(
    request: Request,
    From: Optional[str] = Form(None),
    Body: Optional[str] = Form(None),
    MediaContentType0: Optional[str] = Form(None),
    MediaUrl0: Optional[str] = Form(None),
):
    # Validate that the request is coming from twilio
    validator = RequestValidator(config.twilio_auth_token)
    form_ = await request.form()
    if not validator.validate(
        str(request.url), form_, request.headers.get("X-Twilio-Signature", "")
    ):
        raise HTTPException(status_code=400, detail="Error in Twilio Signature")
    logger.info(
        "/sms %s %s %s %s", str(From), str(Body), str(MediaContentType0), str(MediaUrl0)
    )

    if MediaContentType0 is not None and "image" in MediaContentType0:
        twilio_client.handle_image(From, MediaUrl0)
    else:
        twilio_client.handle_message(From, Body)

    # Empty MessageResponse means don't send a response
    # handle_message will send the reply instead
    response = MessagingResponse()
    return Response(content=str(response), media_type="application/xml")


@app.get("/v/{user_hash}", response_class=HTMLResponse)
def images_page(
    user_hash: str,
    request: Request,
    n: Optional[int] = None,
):
    prompt = None
    if n is not None:
        prompt = db.get_prompt(n)
    else:
        prompt = db.get_current_prompt()
        n = prompt.id

    if not db.get_submission_status(user_hash, n):
        raise HTTPException(status_code=401, detail="No submission for this prompt")

    pics = db.get_pics_by_prompt(n)

    date_str = prompt.date.strftime("%b %-d, %Y")

    return templates.TemplateResponse(
        request=request,
        name="gallery.html",
        context={"pics": pics, "prompt": prompt.prompt, "date": date_str},
    )


@app.get("/h/{user_hash}", response_class=HTMLResponse)
def history_page(user_hash: str):
    pics = db.get_pics_by_hash(user_hash)
    html_list = []
    for pic in pics:
        prompt = db.get_prompt(pic.prompt)
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
