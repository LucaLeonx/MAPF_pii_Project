from benchmark.test import Test


class Benchmark():

    def __init__(self, name="", description="", tests=[]):
        self._name = name
        self._description = description
        self._tests = tests

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def get_tests(self):
        return self._tests
