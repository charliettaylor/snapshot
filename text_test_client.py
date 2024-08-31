from typing import override

from sqlalchemy.orm import Session

from config import Settings, settings
from crud import Crud
from text import TextInterface


class TextTestClient(TextInterface):
    def __init__(self, session: Session, settings: Settings, crud: Crud):
        super().__init__(session, settings, crud)

    @override
    def send_message(self, to: str, text: str):
        print(to, "{}: {}".format(settings.twilio_phone_number, text))

    @override
    def receive_message(self, from_: str, text: str):
        print(from_, text)
        self.handle_message(from_, text)

    @override
    def handle_dev_message(self, from_: str, text: str):
        prompt_text = " ".join(text.split(" ")[1:])
        return prompt_text

if __name__ == "__main__":
    client = TextTestClient()

    while True:
        text = input()
        client.receive_message("9517518340", text)
