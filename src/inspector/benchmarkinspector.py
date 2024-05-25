from benchmark.testdescription import TestDescription
from connection.clientsocket import ClientSocket
from connection.message import Message
from inspector.testinspector import TestInspector
from runner.exceptions import ElementNotFoundException, CustomException


class BenchmarkInspector(object):
    def __init__(self, connection_config):
        self._socket = ClientSocket(connection_config)
        self._test_recorders = []

    # "ping": self.ping,
    # "request_test": self._test_manager.get_test_with_name,
    # "request_random_test": self._test_manager.get_random_unassigned_test,
    # "submit_result"

    def request_test(self, name):

        required_recorder = [recorder for recorder in self._test_recorders if recorder.get_test_description().get_name() == name]

        if required_recorder:
            return required_recorder[0]

        self._socket.send_message(Message("request_test", name))
        response = self._socket.receive_message()

        if response.get_title() == "Error":
            raise ElementNotFoundException("The requested test" + name + " is not available")
        else:
            new_recorder = TestInspector(TestDescription.from_dict(response.get_description()))
            self._test_recorders.append(new_recorder)
            return new_recorder

    def request_random_test(self):
        self._socket.send_message(Message("request_random_test", ""))
        response = self._socket.receive_message()

        if response.get_title() == "Error":
            raise ElementNotFoundException("No test is not available")
        else:
            new_recorder = TestInspector(TestDescription.from_dict(response.get_description()))
            self._test_recorders.append(new_recorder)
            return new_recorder

    def get_recorders(self):
        return self._test_recorders

    def send_result(self, recorder):
        self._socket.send_message(Message("send_result", str(recorder.get_result())))
        response = self._socket.receive_message()

        if response.get_title() == "Error":
            raise CustomException(response.get_content())




