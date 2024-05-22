import json
from abc import ABC, abstractmethod

from connection.message import Message


class Socket(ABC):
    @abstractmethod
    def __init__(self):
        self.socket = None
    
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass
    
    def send_message(self, message):
        self.socket.send_json(message.to_dict())

    def receive_message(self):
        message_dict = self.socket.recv_json()
        return Message.from_dict(message_dict)
