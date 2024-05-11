from abc import ABC, abstractmethod

from database import get_db

HOW_TO_START = "Snapshot: Text START to play."
ENTER_USERNAME = "Snapshot: Text STOP to unsubscribe. To finish registering, please enter your username:"
REGISTRATION_SUCCESSFUL = "Snapshot: You've successfully registered as {}. Thanks! :)"
UNSUBSCRIBED = "Snapshot: You've successfully unsubscribed. Text START to resubscribe."
PROMPT = "Snapshot: {prompt} {link} Week {week} {year} STOP to unsubscribe"

STOP_KEYWORDS = ["STOP", "UNSUBSCRIBE", "OPTOUT"]
START_KEYWORDS = ["START", "PLAY", "OPTIN", "SUBSCRIBE", "RESUBSCRIBE"]

def contains(text: str, words: [str], ignore_case = True):
    for word in words:
        if word in text:
            return True
        if ignore_case and word.lower() in text.lower():
            return True
    return False

class TextInterface(ABC):
    def __init__(self):
        self.db = get_db()

    @abstractmethod
    def send_message(self, to: str, text: str):
        pass
    
    @abstractmethod
    def receive_message(self, from_: str, text: str):
        pass

    def handle_message(self, from_: str, text: str):
        if contains(text, STOP_KEYWORDS):
            self.send_message(from_, UNSUBSCRIBED)

        if contains(text, START_KEYWORDS):
            self.send_message(from_, ENTER_USERNAME)
        
