from typing import override

from config import settings
from text import TextInterface

class TestClient(TextInterface):

    @override
    def send_message(self, to: str, text: str):
        print(to, "{}: text".format(settings.twilio_phone_number))

    @override
    def receive_message(self, from_: str, text: str):
        print(from_, text)


