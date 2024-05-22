from benchmark.commanddispatcher import CommandDispatcher
from connection.message import Message
from connection.serversocket import ServerSocket
from runner.exceptions import CustomException
from runner.testmanager import TestManager


class BenchmarkRunner(object):
    def __init__(self, benchmark, connection_config):
        self._benchmark = benchmark
        self._socket = ServerSocket(connection_config)
        self._test_manager = TestManager(benchmark.get_tests())
        self._command_dispatcher = CommandDispatcher(
            {"ping": self.ping,
             "request_test": self._test_manager.get_test_with_name,
             "assign_test": self._test_manager.assign_test,
             "request_random_test": self._test_manager.get_random_unassigned_test,
             "submit_result": self._test_manager.record_test_result})

    def get_benchmark(self):
        return self._benchmark

    def run_benchmark(self):
        while not self._test_manager.all_tests_done():
            request = self._socket.receive_message()

            try:
                result = self._command_dispatcher.execute(request.get_title(), request.get_content())
                response = Message("OK", result)
            except (AttributeError, CustomException) as e:
                response = Message("Error", str(e))

            self._socket.send_message(response)

        return self.get_results()

    def get_results(self):
        return self._test_manager.get_results()

    @staticmethod
    def ping():
        return "Pong"
