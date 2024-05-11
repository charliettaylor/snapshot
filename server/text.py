from abc import ABC, abstractmethod

from schema import Registration
from database import get_db
from crud import *

HOW_TO_START = "Snapshot: Text START to play."
ENTER_USERNAME = "Snapshot: Text STOP to unsubscribe. To finish registering, please enter your username:"
ENTER_USERNAME_AGAIN = "Snapshot: please enter your username:"
CONFIRM_USERNAME = "Snapshot: You entered \"{}\", text YES to confirm or NO to change."
REGISTRATION_SUCCESSFUL = "Snapshot: You've successfully registered as {}. Thanks! :)"
UNSUBSCRIBED = "Snapshot: You've successfully unsubscribed. Text START to resubscribe."
PROMPT = "Snapshot: {prompt} {link} Week {week} {year} STOP to unsubscribe"

STOP_KEYWORDS = ["STOP", "UNSUBSCRIBE", "OPTOUT"]
START_KEYWORDS = ["START", "PLAY", "OPTIN", "SUBSCRIBE", "RESUBSCRIBE"]

POSITIVE_KEYWORDS = ["YES", "Y", "YE", "YEAH", "YEA", "CONFIRM", "YEP"]
NEGATIVE_KEYWORDS = ["NO", "N", "NOPE", "NAY", "NAH"]

def contains(text: str, words: [str], ignore_case = True):
    for word in words:
        if word in text:
            return True
        if ignore_case and word.lower() in text.lower():
            return True
    return False

class TextInterface(ABC):
    def __init__(self):
        self.db = next(get_db(), None)

    @abstractmethod
    def send_message(self, to: str, text: str):
        pass
    
    @abstractmethod
    def receive_message(self, from_: str, text: str):
        pass

    def handle_message(self, from_: str, text: str):

        reg = get_reg(self.db, from_)
        if reg is None:
            print("Creating registration...")
            reg = create_reg(self.db, from_)

        if contains(text, STOP_KEYWORDS):
            self.send_message(from_, UNSUBSCRIBED)

        elif reg.state == 0 and contains(text, START_KEYWORDS):
            update_reg(self.db, Registration(phone=from_, username=None, state=1))
            self.send_message(from_, ENTER_USERNAME)

        elif reg.state == 0:
            self.send_message(from_, HOW_TO_START)

        elif reg.state == 1:
            update_reg(self.db, Registration(phone=from_, username=None, state=2))
            self.send_message(from_, CONFIRM_USERNAME.format(text))

        elif reg.state == 2 and contains(text, POSITIVE_KEYWORDS):
            update_reg(self.db, Registration(phone=from_, username=None, state=3))
            self.send_message(from_, REGISTRATION_SUCCESSFUL.format(reg.username))

        elif reg.state == 2 and contains(text, NEGATIVE_KEYWORDS):
            update_reg(self.db, Registration(phone=from_, username=None, state=1))
            self.send_message(from_, ENTER_USERNAME_AGAIN)

        
