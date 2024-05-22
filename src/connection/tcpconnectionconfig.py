from connection.connectionconfig import ConnectionConfig


class TCPConnectionConfig(ConnectionConfig):
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def get_address(self):
        return "tcp://{}:{}".format(self._host, self._port)

    def get_host(self):
        return self._host

    def get_port(self):
        return self._port
