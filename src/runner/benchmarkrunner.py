from typing import Dict, List

from connection.connectionconfig import ConnectionConfig, TCPConnectionConfig
from description.benchmarkdescription import BenchmarkDescription
from result.testrun import TestRun
from commanddispatcher import CommandDispatcher
from connection.message import Message
from connection.socket import ServerSocket
from exceptions import CustomException
from runner.testmanager import TestManager


class BenchmarkRunner(object):
    def __init__(self, benchmark: BenchmarkDescription,
                 connection_config: ConnectionConfig = TCPConnectionConfig(host='localhost', port=9361)):
        self._benchmark = benchmark
        self._socket = ServerSocket(connection_config)
        self._test_manager = TestManager(benchmark.test_occurrences)
        self._stop_event = False
        self._command_dispatcher = CommandDispatcher(
            {"ping": self.ping,
             "request_test": self.request_test,
             "request_random_test": self.request_random_test,
             "submit_result": self.submit_result})

    def get_benchmark(self) -> BenchmarkDescription:
        return self._benchmark

    def start_benchmark(self):
        # Initialization
        self._socket.open()
        # request = None
        # self._stop_event = False

        while not self._test_manager.all_tests_done():
            # Wait for message, or stop if received stop_benchmark()
            #while not self._socket.poll(timeout=1000):
            #    if self._stop_event:
            #        self._socket.close()
            #        return

            request = self._socket.receive_message()

        # Try to execute command and determine response
            try:
                result = self._command_dispatcher.execute(request.title, request.content)
                response = Message("OK", result)
            except (AttributeError, CustomException) as e:
                print("Exception returned: " + str(e))
                response = Message("Error", str(e))
            # Send response
            self._socket.send_message(response)

        # End communication
        self._socket.close()

    def stop_benchmark(self):
        self._stop_event = True

    def get_results(self) -> dict[str, list[TestRun]]:
        return self._test_manager.get_results()

    @staticmethod
    def ping():
        return "Pong"

    def request_test(self, test_name):
        test_description = self._test_manager.get_test_with_name(test_name)
        return test_description.to_dict()

    def request_random_test(self):
        test_description = self._test_manager.get_random_unassigned_test()
        return test_description.to_dict()

    def submit_result(self, result_dict):
        result = TestRun.from_dict(result_dict)
        self._test_manager.record_test_result(result)
        return ""


