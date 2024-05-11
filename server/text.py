from abc import ABC, abstractmethod

class TextInterface(ABC):

    @abstractmethod
    def send_message(self, to: str, text: str):
        pass
    
    @abstractmethod
    def receive_message(self, from_: str, text: str):
        pass

    def handle_message(self, from_: str, text: str):
        pass
        
