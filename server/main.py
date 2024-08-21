from typing import Generator

from fastapi import Depends, FastAPI, UploadFile, Form, Response
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

@app.post('/upload/{user_hash}')
def upload(user_hash: str, file: UploadFile, db: Session = Depends(get_db)):
    user = crud.get_user_by_hash(db, user_hash)

    if user is None:
        raise HTTPException(status_code=400, detail="Invalid user")

    return crud.create_pic(db, user.username, file)

@app.post("/sms")
def receive_message(from_: str = Form(...), body: str = Form(...)):
    response = MessagingResponse() 
    msg = response.message(f"Hi {from_}, you said: {body}")
    twilio_client.receive_message(from_, body)
    return Response(content=str(response), media_type="application/xml")
    # twilio_client.send_message(from_, "Received message {}".format(body))
