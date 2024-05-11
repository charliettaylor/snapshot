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


