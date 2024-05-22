import zmq
import json

from connection.message import Message
from connection.socket import Socket


class ServerSocket(Socket):
    def __init__(self, connection_config):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self._connection_config = connection_config

    def start(self):
        self.socket.bind(self._connection_config.get_address())

    def stop(self):
        pass


