import json
from abc import ABC, abstractmethod

import zmq

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


class ServerSocket(Socket):
    def __init__(self, connection_config):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self._connection_config = connection_config

    def start(self):
        self.socket.bind(self._connection_config.address)

    def stop(self):
        pass


class ClientSocket(Socket):

    def __init__(self, connection_config):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self._connection_config = connection_config

    def start(self):
        self.socket.connect(self._connection_config.address)

    def stop(self):
        pass
