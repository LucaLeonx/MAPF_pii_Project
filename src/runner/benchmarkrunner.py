from result.testrun import TestRun
from runner.commanddispatcher import CommandDispatcher
from connection.message import Message
from connection.serversocket import ServerSocket
from exceptions import CustomException
from runner.testmanager import TestManager


class BenchmarkRunner(object):
    def __init__(self, benchmark, connection_config):
        self._benchmark = benchmark
        self._socket = ServerSocket(connection_config)
        self._test_manager = TestManager(benchmark.get_tests())
        self._command_dispatcher = CommandDispatcher(
            {"ping": self.ping,
             "request_test": self.request_test,
             "request_random_test": self.request_random_test,
             "submit_result": self.submit_result})

    def get_benchmark(self):
        return self._benchmark

    def run_benchmark(self):
        self._socket.start()
        while not self._test_manager.all_tests_done():
            request = self._socket.receive_message()
            print("In the loop")
            try:
                result = self._command_dispatcher.execute(request.get_title(), request.get_content())
                response = Message("OK", result)
            except (AttributeError, CustomException) as e:
                print("Exception returned: " + str(e))
                response = Message("Error", str(e))

            self._socket.send_message(response)

        return self.get_results()

    def get_results(self):
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


