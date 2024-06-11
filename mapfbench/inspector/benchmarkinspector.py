from typing import List

from connection.connectionconfig import TCPConnectionConfig, ConnectionConfig
from connection.message import Message
from connection.c_socket import ClientSocket
from description.benchmarkdescription import TestDescription
from inspector.testinspector import TestInspector
from utilities.customexceptions import ElementNotFoundException, CustomException


class BenchmarkInspector(object):
    """
        The BenchmarkInspector is the link between
        the BenchmarkRunner server providing the tests
        and the client program running them
    """
    def __init__(self, connection_config: ConnectionConfig = TCPConnectionConfig(host='localhost', port=9361)):
        """
            Object initializer

            Parameters
            ----------
            connection_config : ConnectionConfig, optional
                The configuration for the connection to the BenchmarkRunner
        """
        self._socket = ClientSocket(connection_config)
        self._test_recorders = []

    def start(self):
        """
            Starts the BenchmarkInspector, opening a connection to the server
        """
        self._socket.open()

    def stop(self):
        """
            Stops the BenchmarkInspector, closing the connection to the server
        """
        self._socket.close()

    def request_test(self, name: str) -> TestInspector:
        """
            Requests a test with the specified name from the BenchmarkRunner,
            in order to solve it.

            Parameters
            ----------
            name: str
                The name of the requested test

            Returns
            -------
            TestInspector
                The inspector associated to the corresponding test instance

            Raises
            ------
            ElementNotFoundException
                If the requested test doesn't exist or all instances of the requested test
                have been assigned
        """
        required_recorder = [recorder for recorder in self._test_recorders if recorder.get_test_description().get_name() == name]

        if required_recorder:
            return required_recorder[0]

        self._socket.send_message(Message("request_test", name))
        response = self._socket.receive_message()

        if response.title == "Error":
            raise ElementNotFoundException("The requested test " + name + " is not available")
        else:
            new_recorder = TestInspector(TestDescription.from_dict(response.content))
            self._test_recorders.append(new_recorder)
            return new_recorder

    def request_random_test(self) -> TestInspector:
        """
            Request a random test instance to the BenchmarkRunner

            Returns
            -------
            TestInspector
                The inspector associated to the received test instance

            Raises
            ------
            ElementNotFoundException
                If all tests of the benchmark have been assigned
        """
        self._socket.send_message(Message("request_random_test", ""))
        response = self._socket.receive_message()
        if response.title == "Error":
            if response.content.startswith("All tests have been assigned"):
                raise ElementNotFoundException("No test is not available")
            else:
                raise
        else:
            new_recorder = TestInspector(TestDescription.from_dict(response.content))
            self._test_recorders.append(new_recorder)
            return new_recorder

    def get_recorders(self) -> List[TestInspector]:
        """
            Returns the list of the inspectors of the requested tests

            Returns
            -------
            List[TestInspector]
                A list of the inspectors of the requested tests
        """
        return self._test_recorders

    def submit_result(self, inspector: TestInspector):
        """
            Send the result of a test instance back to the BenchmarkServer

            Parameters
            ----------
            inspector : TestInspector
                The inspector with the associated test data
        """
        self._socket.send_message(Message("submit_result", inspector.get_result().to_dict()))
        response = self._socket.receive_message()

        if response.title == "Error":
            raise CustomException(response.content)




