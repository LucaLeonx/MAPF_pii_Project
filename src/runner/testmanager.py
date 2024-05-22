from random import random
from runner.exceptions import ElementNotFoundException
from runner.testrecord import TestRecord


class TestManager:
    def __init__(self, tests):
        self._test_records = [TestRecord(test) for test in tests]

    def get_test_records(self):
        return self._test_records

    def get_test_record_by_name(self, test_name):
        requested_test = [record for record in self._test_records if record.get_test_name() == test_name]

        if not requested_test:
            raise ElementNotFoundException("No test with name " + test_name + "is available")

        return requested_test[0]

    def get_test_with_name(self, test_name):
        return self.get_test_record_by_name(test_name).get_test()

    def assign_test(self, test_name):
        requested_test = self.get_test_with_name(test_name)
        requested_test.assign_test()

    def record_test_result(self, result):
        finished_test = self.get_test_record_by_name(result.get_test_name())
        finished_test.record_result(result)

    def get_random_unassigned_test(self):
        unassigned_tests = [test for test in self._test_records if not test.is_assigned()]

        if not unassigned_tests:
            raise ElementNotFoundException("All tests have been assigned")

        return random.choice(unassigned_tests)

    def all_tests_assigned(self):
        return all(test.is_assigned() for test in self._test_records)

    def all_tests_done(self):
        return all(test.is_done() for test in self._test_records)

    def get_results(self):
        return [test.get_result() for test in self._test_records]





