from twilio.rest import Client
from typing import override

from config import settings
from text import TextInterface

class SmsClient(TextInterface):
    def __init__(self):
        super().__init__()
        self.client = Client(settings.twilio_account_sid, settings.twilio_auth_token)

    @override
    def send_message(self, to: str, text: str):
        self.client.messages.create(to=to, from_=settings.twilio_phone_number, body=text)

    @override
    def receive_message(self, from_: str, text: str):
        print(from_, text)

if __name__ == "__main__":
    client = SmsClient()

    # client.send_message("+19517518340", "Tester McTesty")

    while True:
        client.receive_message("+19517518340", "test")
