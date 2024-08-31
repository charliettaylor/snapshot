import logging
from typing import override

from fastapi import HTTPException
from sqlalchemy.orm import Session
from twilio.rest import Client

from constants import DEV_ENV
from config import Settings, settings
from crud import Crud
from text import TextInterface

logger = logging.getLogger(__name__)


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

    @override
    def handle_dev_message(self, from_: str, text: str) -> str:
        prompt_text = " ".join(text.split(" ")[1:])
        logger.info("handle_dev_message %s", prompt_text)
        if config.environment != DEV_ENV:
            logger.info("text routed to dev env")
            raise HTTPException(status_code=501, detail="dev code detected.")
        if from_ not in config.dev_allowlist.split(","):
            logger.info(
                "%s attempted to use DEV environment but was not allowlisted.", from_
            )
            raise HTTPException(status_code=401, detail="Number not allowlisted.")
        return prompt_text
