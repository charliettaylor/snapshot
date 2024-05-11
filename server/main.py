from fastapi import FastAPI
from twilio.rest import Client as TwilioClient

from config import settings

twilio_client = TwilioClient(settings.twilio_account_sid, settings.twilio_auth_token)

message = twilio_client.messages.create(
    to="+19517518340",
    from="+16802204458",
    body="Hello from Python!")

print(message.sid)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


