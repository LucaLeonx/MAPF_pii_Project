import json
import zmq

from connection.message import Message
from connection.socket import Socket


class ClientSocket(Socket):

    def __init__(self, connection_config):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self._connection_config = connection_config

    def start(self):
        self.socket.connect(self._connection_config.get_address())

    def stop(self):
        pass
