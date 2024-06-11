import signal
import threading
from typing import Dict, List, Any

from connection.connectionconfig import ConnectionConfig, TCPConnectionConfig
from description.benchmarkdescription import BenchmarkDescription
from result.testrun import TestRun, BenchmarkRun
from commanddispatcher import CommandDispatcher
from connection.message import Message
from connection.c_socket import ServerSocket
from utilities.customexceptions import CustomException
from runner.testmanager import TestManager


class BenchmarkRunner(object):
    def __init__(self, benchmark: BenchmarkDescription,
                 connection_config: ConnectionConfig = TCPConnectionConfig(host='localhost', port=9361)):
        self._benchmark = benchmark
        self._socket = ServerSocket(connection_config)
        self._test_manager = TestManager(benchmark.test_occurrences)
        self._command_dispatcher = CommandDispatcher(
            {"ping": self.ping,
             "request_test": self.request_test,
             "request_random_test": self.request_random_test,
             "submit_result": self.submit_result})

    def get_benchmark(self) -> BenchmarkDescription:
        return self._benchmark

    def start_benchmark(self):
        # signal.signal(signal.SIGTERM, self._shutdown)
        try:
            self._socket.open()
            print("Benchmark started")

            while not self._test_manager.all_tests_done():
                request = self._socket.receive_message()
                response = None
                try:
                    result = self._command_dispatcher.execute(request.title, request.content)
                    response = Message("OK", result)
                except (AttributeError, CustomException) as e:
                    print("Exception returned: " + str(e))
                    response = Message("Error", str(e))
                finally:
                    self._socket.send_message(response)
        finally:
            # End communication
            self.stop_benchmark()

    def stop_benchmark(self):
        self._socket.close()

    def get_results(self) -> BenchmarkRun:
        return BenchmarkRun(self.get_benchmark(), self._test_manager.get_results())

    def get_tests_left(self):
        return self._test_manager.get_number_of_tests_left()

    @staticmethod
    def ping():
        return "Pong"

    def request_test(self, test_name):
        test_description = self._test_manager.get_test_with_name(test_name)
        return test_description.to_dict()

    def request_random_test(self, content=None):
        test_description = self._test_manager.get_random_unassigned_test()
        return test_description.to_dict()

    def submit_result(self, result_dict: dict[str, Any]):
        result = TestRun.from_dict(result_dict)
        self._test_manager.record_test_result(result)
        return ""
