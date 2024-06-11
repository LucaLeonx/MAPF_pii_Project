import random

from description.benchmarkdescription import TestDescription

from result.testrun import TestRun
from runner.testrecord import TestRecord
from utilities.customexceptions import ElementNotFoundException


class TestManager:
    def __init__(self, tests: dict[TestDescription, int]):
        self._test_records = [TestRecord(test[0], test[1]) for test in tests.items()]

    def get_test_records(self) -> list[TestRecord]:
        return self._test_records

    def get_test_record_by_name(self, test_name: str) -> TestRecord:
        requested_test = [record for record in self._test_records if record.test_name == test_name]

        if not requested_test:
            raise ElementNotFoundException("No test with name " + test_name + "is available")

        return requested_test[0]

    def get_test_with_name(self, test_name: str) -> TestDescription:
        return self.get_test_record_by_name(test_name).test

    def record_test_result(self, result: TestRun) -> None:
        finished_test = self.get_test_record_by_name(result.test_description.name)
        finished_test.register_result(result)

    def get_random_unassigned_test(self) -> TestDescription:
        available_tests = [test for test in self._test_records if not test.all_iterations_assigned()]

        # if not available_tests:
        #    available_tests = [test for test in self._test_records if not test.is_done()]

        if not available_tests:
            raise ElementNotFoundException("All tests have been assigned")

        chosen_test = random.choice(available_tests)
        return chosen_test.test

    def get_number_of_tests_left(self) -> dict[str, int]:
        tests_left = {}
        for record in self._test_records:
            tests_left.update({record.test_name: record.remaining_occurrences})

        return tests_left

    def all_tests_done(self) -> bool:
        return all(test.is_done() for test in self._test_records)

    # TODO: add integer index to iterations of same test
    def get_results(self) -> dict[str, list[TestRun]]:
        return dict([(record.test_name, record.get_results()) for record in self._test_records])





