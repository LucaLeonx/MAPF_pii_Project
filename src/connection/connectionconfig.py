from abc import ABC, abstractmethod


class ConnectionConfig(ABC):
    @abstractmethod
    def get_address(self):
        pass
