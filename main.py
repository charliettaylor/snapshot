# pyright: reportCallInDefaultInitializer=false

import logging
from typing import Annotated

from fastapi import Cookie, FastAPI, Form, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

import models
from config import settings
from constants import *
from database import Database, engine
from SmsClient import SmsClient

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)  # pyright: ignore [reportAny]

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
    From: str | None = Form(None),
    Body: str | None = Form(None),
    MediaContentType0: str | None = Form(None),
    MediaUrl0: str | None = Form(None),
):
    # Validate that the request is coming from twilio
    validator = RequestValidator(settings.twilio_auth_token)
    form_ = await request.form()

    if not validator.validate(  # pyright: ignore [reportUnknownMemberType]
        str(request.url), form_, request.headers.get("X-Twilio-Signature", "")
    ):
        raise HTTPException(status_code=400, detail="Error in Twilio Signature")
    logger.info(
        "/sms %s %s %s %s", str(From), str(Body), str(MediaContentType0), str(MediaUrl0)
    )

    if From is None:
        raise HTTPException(status_code=400, detail="Unable to identify sender")

    if (
        MediaContentType0 is not None
        and "image" in MediaContentType0
        and MediaUrl0 is not None
    ):
        twilio_client.handle_image(From, MediaUrl0)
    elif Body is not None:
        twilio_client.handle_message(From, Body)

    # Empty MessageResponse means don't send a response
    # handle_message will send the reply instead
    response = MessagingResponse()
    return Response(content=str(response), media_type="application/xml")


@app.get("/v/{user_hash}", response_class=HTMLResponse)
def images_page(
    request: Request,
    user_hash: str,
    n: int | None = None,
):
    if n is not None:
        prompt = db.get_prompt(n)
    else:
        prompt = db.get_current_prompt()

    if prompt is None:
        raise HTTPException(status_code=404, detail="Unable to find prompt")

    if not db.get_submission_status(
        user_hash, prompt.id  # pyright: ignore [reportArgumentType]
    ):
        raise HTTPException(status_code=401, detail="No submission for this prompt")

    pics = db.get_pics_by_prompt(prompt.id)  # pyright: ignore [reportArgumentType]

    pics = [vars(pic) for pic in pics]
    for pic in pics:
        pic["click_url"] = pic["url"]

    date_str: str = prompt.date.strftime("%b %-d, %Y")  # pyright: ignore [reportAny]

    og = {"display": False}
    winner = db.get_winner_by_prompt(prompt.id)  # pyright: ignore [reportArgumentType]
    if winner is not None:
        og["display"] = True
        og["url"] = winner.url

    return templates.TemplateResponse(
        request=request,
        name="gallery.html",
        context={"pics": pics, "prompt": prompt.prompt, "date": date_str, "og": og},
    )


@app.get("/h/{user_hash}", response_class=HTMLResponse)
def history_page(user_hash: str):
    pics = db.get_pics_by_hash(user_hash)
    html_list: list[str] = []
    for pic in pics:
        prompt = db.get_prompt(pic.prompt)  # pyright: ignore [reportArgumentType]
        assert prompt is not None
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


@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request, password: Annotated[str | None, Cookie()] = None):
    if not is_logged_in(password):
        raise HTTPException(status_code=401, detail="Unauthorized")

    prompts = db.get_all_prompts()
    prompts = [vars(prompt) for prompt in prompts]
    for prompt in prompts:
        prompt["url"] = BASE_URL + "a?n={}".format(prompt["id"])

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={"prompts": prompts},
    )


@app.get("/a", response_class=HTMLResponse)
def winner_admin_page(
    request: Request,
    n: int | None = None,
    password: Annotated[str | None, Cookie()] = None,
):
    if not is_logged_in(password):
        raise HTTPException(status_code=401, detail="Unauthorized")

    prompt = None
    if n is None:
        prompt = db.get_current_prompt()
    else:
        prompt = db.get_prompt(n)

    if prompt is None:
        raise HTTPException(status_code=404, detail="Unable to find prompt")

    pics = db.get_pics_by_prompt(prompt.id)  # pyright: ignore [reportArgumentType]
    pics = [vars(pic) for pic in pics]
    for pic in pics:
        pic["click_url"] = BASE_URL + "win/{}".format(pic["id"])

    date_str: str = prompt.date.strftime("%b %-d, %Y")  # pyright: ignore [reportAny]

    return templates.TemplateResponse(
        request=request,
        name="gallery.html",
        context={
            "pics": pics,
            "prompt": prompt.prompt,
            "date": date_str,
            "og": {"display": False},
        },
    )


@app.get("/win/{pic_id}")
def set_winner(pic_id: int, password: Annotated[str | None, Cookie()] = None):
    if not is_logged_in(password):
        raise HTTPException(status_code=401, detail="Unauthorized")

    if db.set_winner(pic_id) is not None:
        return RedirectResponse(url="/admin", status_code=303)

    raise HTTPException(status_code=404, detail="Pic not found")

@app.post("/prompt")
async def create_prompt(request: Request, password: Annotated[str | None, Cookie()] = None) -> RedirectResponse:
    if not is_logged_in(password):
        raise HTTPException(status_code=401, detail="Unauthorized")

    body = await request.form()
    prompt = str(body.get("prompt"))
    if prompt is None:
        raise HTTPException(status_code=400, detail="No prompt provided")

    db.create_prompt(prompt)
 
    return RedirectResponse(url="/admin", status_code=303)

def is_logged_in(password: str | None):
    return password is not None and password == settings.admin_pass
