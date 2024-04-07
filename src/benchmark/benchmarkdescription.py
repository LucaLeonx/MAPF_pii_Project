
class BenchmarkDescription:

    def __init__(self, name, description="", tests=[]):
        if name != "":
            self._name = name
        else:
            raise ValueError("Benchmark name cannot be empty")

        self._description = description
        self._tests = tests

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def get_tests(self):
        return self._tests
