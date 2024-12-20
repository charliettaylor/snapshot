from typing import override

from Client import Client
from config import Settings, settings
from database import Database


class TextTestClient(Client):
    def __init__(self, settings: Settings, db: Database | None = None):
        super().__init__(settings, db)

    @override
    def send_message(self, to: str, text: str):
        print(to, "{}: {}".format(settings.twilio_phone_number, text))

    @override
    def receive_message(self, from_: str, text: str):
        print(from_, text)
        self.handle_message(from_, text)

    @override
    def handle_beta_message(self, from_: str, text: str):
        return text


if __name__ == "__main__":
    client = TextTestClient(settings)

    while True:
        text = input()
        client.receive_message("9517518340", text)
