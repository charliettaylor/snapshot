from typing import override

from config import settings
from text import TextInterface


class TestClient(TextInterface):

    @override
    def send_message(self, to: str, text: str):
        print(to, "{}: {}".format(settings.twilio_phone_number, text))

    @override
    def receive_message(self, from_: str, text: str):
        print(from_, text)
        self.handle_message(from_, text)


if __name__ == "__main__":
    client = TestClient()

    while True:
        text = input()
        client.receive_message("9517518340", text)
