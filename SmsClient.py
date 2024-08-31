import logging
from typing import override

from fastapi import HTTPException
from sqlalchemy.orm import Session
from twilio.rest import Client as TwilioClient

from Client import Client
from database import Database
from config import Settings, settings
from constants import DEV_ENV

logger = logging.getLogger(__name__)


class SmsClient(Client):
    def __init__(self, settings: Settings, db: Database | None = None):
        super().__init__(settings, db)
        self.twilio_client = TwilioClient(
            settings.twilio_account_sid, settings.twilio_auth_token
        )

    @override
    def send_message(self, to: str, text: str) -> None:
        self.twilio_client.messages.create(
            to=to, from_=settings.twilio_phone_number, body=text
        )

    @override
    def receive_message(self, from_: str, text: str) -> None:
        print(from_, text)

    @override
    def handle_dev_message(self, from_: str, text: str) -> str:
        prompt_text = " ".join(text.split(" ")[1:])
        logger.info("handle_dev_message %s", prompt_text)
        if self.settings.environment != DEV_ENV:
            logger.info("text routed to dev env")
            raise HTTPException(status_code=501, detail="dev code detected.")
        if from_ not in self.settings.dev_allowlist.split(","):
            logger.info(
                "%s attempted to use DEV environment but was not allowlisted.", from_
            )
            raise HTTPException(status_code=401, detail="Number not allowlisted.")
        return prompt_text
