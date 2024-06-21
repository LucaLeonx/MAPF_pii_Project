from abc import ABC, abstractmethod
from typing import Any

import msgpack
import zmq


class Socket(ABC):

    def __init__(self, address: str):
        self._context = zmq.Context.instance()
        self._address = address
        self._socket = None
        self._stop = True

    @abstractmethod
    def start(self):
        pass

    def stop(self):
        self._stop = True
        self._socket.close()

    def send_message(self, label: str, content: Any = ""):
        message = {"label": label, "content": content}
        self._socket.send(msgpack.dumps(message))

    def receive_message(self) -> dict[str, Any]:
        # This gives back command to the Python interpreter after each timeout,
        # making possible to stop it (otherwise, it may get stuck in the C code
        # of the ZMQ library
        while not self._socket.poll(timeout=1000):
            if self._stop:
                break

        received = msgpack.loads(self._socket.recv())
        return received


class ServerSocket(Socket):

    def __init__(self, address: str):
        super().__init__(address)
        self._socket = self._context.socket(zmq.REP)

    def start(self):
        self._socket.bind(self._address)


class ClientSocket(Socket):

    def __init__(self, address: str):
        super().__init__(address)
        self._socket = self._context.socket(zmq.REQ)

    def start(self):
        self._socket.connect(self._address)
