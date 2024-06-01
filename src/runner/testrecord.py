from description.benchmarkdescription import TestDescription
from exceptions import OperationAlreadyDoneException, ElementNotAvailableException
from result.testrun import TestRun


class TestRecord(object):
    def __init__(self, test: TestDescription, occurrences: int):
        self._results = []
        self._test = test
        self._remaining_occurrences = occurrences

    @property
    def test(self) -> TestDescription:
        return self._test

    @property
    def test_name(self) -> str:
        return self._test.name

    @property
    def remaining_occurrences(self) -> int:
        return self._remaining_occurrences

    def is_done(self) -> bool:
        return self._remaining_occurrences == 0

    def register_result(self, result) -> None:
        if not self.is_done():
            self._remaining_occurrences -= 1
            self._results.append(result)
        else:
            raise OperationAlreadyDoneException("Test already done")

    def get_results(self) -> list[TestRun]:
        return self._results
