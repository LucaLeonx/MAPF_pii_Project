from random import random

from description.benchmarkdescription import TestDescription
from exceptions import ElementNotFoundException
from result.testrun import TestRun
from runner.testrecord import TestRecord


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
        unassigned_tests = [test for test in self._test_records if not test.is_done()]

        if not unassigned_tests:
            raise ElementNotFoundException("All tests have been assigned")

        return random.choice(unassigned_tests)

    def all_tests_done(self) -> bool:
        return all(test.is_done() for test in self._test_records)

    # TODO: add integer index to iterations of same test
    def get_results(self) -> dict[str, list[TestRun]]:
        return dict([(record.test_name, record.get_results()) for record in self._test_records])





