import json
from abc import ABC, abstractmethod

import zmq

from connection.message import Message


class Socket(ABC):
    @abstractmethod
    def __init__(self):
        self._socket = None

    @abstractmethod
    def open(self):
        pass

    def close(self):
        self._socket.close()

    def send_message(self, message):
        self._socket.send_json(message.to_dict())

    def receive_message(self):
        message_dict = self._socket.recv_json()
        return Message.from_dict(message_dict)

    def poll(self, timeout=1000):
        self._socket.poll(timeout)


class ServerSocket(Socket):
    def __init__(self, connection_config):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)
        self._connection_config = connection_config

    def open(self):
        self._socket.bind(self._connection_config.address)

    def close(self):
        self._context.term()
        super().close()


class ClientSocket(Socket):

    def __init__(self, connection_config):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REQ)
        self._connection_config = connection_config

    def open(self):
        self._socket.connect(self._connection_config.address)

    def close(self):
        self._context.term()
        super().close()
