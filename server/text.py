from abc import ABC, abstractmethod

from server import get_db

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
        if "STOP" in text:
            self.send_message(from_, "unsubscribed")
        
