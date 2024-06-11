from abc import ABC, abstractmethod


class ConnectionConfig(ABC):
    """
        Data class for the configuration of a connection
    """
    @property
    @abstractmethod
    def address(self):
        """
            The address of the connection
        """
        pass


class TCPConnectionConfig(ConnectionConfig):
    """
        Data class representing the configuration of a TCP connection
    """
    def __init__(self, host: str, port: int):
        """
            Object initializer

            Parameters
            ----------
            host : str
                The hostname used for the connection
            port : int
                The port used for the connection
        """
        self._host = host
        self._port = port

    @property
    def address(self) -> str:
        """
            The full TCP address of the connection
        """
        return "tcp://{}:{}".format(self.host, self.port)

    @property
    def host(self) -> str:
        """
            The hostname of the connection
        """
        return self._host

    @property
    def port(self) -> int:
        """
            The port of the connection
        """
        return self._port
