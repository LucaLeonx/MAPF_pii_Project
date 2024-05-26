from abc import ABC, abstractmethod


class ConnectionConfig(ABC):
    @property
    @abstractmethod
    def address(self):
        pass


class TCPConnectionConfig(ConnectionConfig):
    def __init__(self, host, port):
        self._host = host
        self._port = port

    @property
    def address(self):
        return "tcp://{}:{}".format(self.host, self.port)

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port
