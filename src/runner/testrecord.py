from exceptions import OperationAlreadyDoneException, ElementNotAvailableException


class TestRecord(object):
    def __init__(self, test):
        self._result = None
        self._test = test
        self._assigned = False
        self._is_done = False

    def is_assigned(self):
        return self._assigned

    def is_done(self):
        return self._is_done

    def assign_test(self):
        if not self._assigned:
            self._assigned = True
        else:
            raise OperationAlreadyDoneException("Test already assigned")

    def register_result(self, result):
        if not self._is_done:
            self._is_done = True
            self._result = result
        else:
            raise OperationAlreadyDoneException("Test already done")

    @property
    def test(self):
        return self._test

    @property
    def test_name(self):
        return self._test.name

    def get_result(self):
        if self._is_done:
            return self._result
        else:
            raise ElementNotAvailableException("Test has not result yet")
