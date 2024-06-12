from abc import ABC, abstractmethod

import zmq
import zmq.asyncio
from connection.message import Message


class Socket(ABC):
    @abstractmethod
    def __init__(self, connection_config):
        self._connection_config = connection_config
        self._context = zmq.Context()
        self._socket = None

    @abstractmethod
    def open(self):
        pass

    def close(self):
        self._socket.close()

    def send_message(self, message):
        self._socket.send_json(message.to_dict())

    def receive_message(self) -> Message:
        while not self._socket.poll(timeout=1000):
            continue

        received = self._socket.recv_json()
        return Message.from_dict(received)

    def poll(self, timeout=1000):
        return self._socket.poll(timeout)


class ServerSocket(Socket):
    def __init__(self, connection_config):
        super().__init__(connection_config)
        self._socket = self._context.socket(zmq.REP)

    def open(self):
        self._socket.bind(self._connection_config.address)

    def close(self):
        super().close()
        # self._context.term()


class ClientSocket(Socket):

    def __init__(self, connection_config):
        super().__init__(connection_config)
        self._socket = self._context.socket(zmq.REQ)

    def open(self):
        self._socket.connect(self._connection_config.address)

    def close(self):
        self._context.term()
        super().close()
