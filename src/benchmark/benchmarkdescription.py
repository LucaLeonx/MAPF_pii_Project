from benchmark.testdescription import TestDescription


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

    def to_dict(self):
        return {"name": self._name,
                "description": self._description,
                "tests": [test.to_dict() for test in self.get_tests()]}

    @staticmethod
    def from_dict(dictionary, use_coordinates=False):
        return BenchmarkDescription(dictionary["name"], dictionary["description"],
                                    [TestDescription.from_dict(test, use_coordinates)
                                     for test in dictionary["tests"]])
