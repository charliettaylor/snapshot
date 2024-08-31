from typing import override

from sqlalchemy.orm import Session
from twilio.rest import Client

from config import Settings, settings
from crud import Crud
from text import TextInterface


class SmsClient(TextInterface):
    def __init__(self, session: Session, settings: Settings):
        super().__init__(session, settings)
        self.client = Client(settings.twilio_account_sid, settings.twilio_auth_token)

    @override
    def send_message(self, to: str, text: str) -> None:
        self.client.messages.create(
            to=to, from_=settings.twilio_phone_number, body=text
        )

    @override
    def receive_message(self, from_: str, text: str) -> None:
        print(from_, text)
