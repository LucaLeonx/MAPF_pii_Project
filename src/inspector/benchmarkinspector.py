from connection.connectionconfig import TCPConnectionConfig, ConnectionConfig
from connection.message import Message
from connection.socket import ClientSocket
from description.benchmarkdescription import TestDescription
from inspector.testinspector import TestInspector
from exceptions import ElementNotFoundException, CustomException


class BenchmarkInspector(object):
    def __init__(self, connection_config: ConnectionConfig = TCPConnectionConfig(host='localhost', port=9361)):
        self._socket = ClientSocket(connection_config)
        self._test_recorders = []

    # "ping": self.ping,
    # "request_test": self._test_manager.get_test_with_name,
    # "request_random_test": self._test_manager.get_random_unassigned_test,
    # "submit_result"

    def start(self):
        self._socket.open()

    def stop(self):
        self._socket.close()

    def request_test(self, name):

        required_recorder = [recorder for recorder in self._test_recorders if recorder.get_test_description().get_name() == name]

        if required_recorder:
            return required_recorder[0]

        self._socket.send_message(Message("request_test", name))
        response = self._socket.receive_message()

        if response.title == "Error":
            print(response.content)
            raise ElementNotFoundException("The requested test " + name + " is not available")
        else:
            new_recorder = TestInspector(TestDescription.from_dict(response.content))
            self._test_recorders.append(new_recorder)
            return new_recorder

    def request_random_test(self):
        self._socket.send_message(Message("request_random_test", ""))
        response = self._socket.receive_message()

        if response.title == "Error":
            raise ElementNotFoundException("No test is not available")
        else:
            new_recorder = TestInspector(TestDescription.from_dict(response.content))
            self._test_recorders.append(new_recorder)
            return new_recorder

    def get_recorders(self):
        return self._test_recorders

    def submit_result(self, recorder):
        self._socket.send_message(Message("submit_result", recorder.get_result().to_dict()))
        response = self._socket.receive_message()

        if response.title == "Error":
            raise CustomException(response.content)




