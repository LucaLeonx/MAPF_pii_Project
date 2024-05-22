
class TestRecord(object):
    def __init__(self, test):
        self._result = None
        self._test = test
        self._assigned = False
        self._is_done = False

    def assign_test(self):
        if not self._assigned:
            self._assigned = True
            return True

        return False

    def record_result(self, result):
        if not self._is_done:
            self._is_done = True
            self._result = result
        else:
            raise Exception("Test was already concluded")

    def get_test(self):
        return self._test

    def get_result(self):
        if self._is_done:
            return self._result
        else:
            raise Exception("Test has not result yet")



