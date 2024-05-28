import pytest

from description.benchmarkdescription import BenchmarkDescription
from exceptions import EmptyElementException, InvalidElementException

import globals

benchmark_description = globals.benchmark_description()
default_test = globals.test_description()


class TestBenchmarkDescription:

    def test_init_guards(self):
        with pytest.raises(EmptyElementException) as excinfo:
            benchmark = BenchmarkDescription("No-tests", {})
        assert "Benchmark must have at least one test" in str(excinfo)

        with pytest.raises(InvalidElementException) as excinfo:
            benchmark = BenchmarkDescription("Zero iterations", {default_test: 0})
        assert "Number of occurrences for each test must be positive" in str(excinfo)

        with pytest.raises(InvalidElementException) as excinfo:
            benchmark = BenchmarkDescription("Negative iterations", {default_test: -1})
        assert "Number of occurrences for each test must be positive" in str(excinfo)

        with pytest.raises(EmptyElementException) as excinfo:
            benchmark = BenchmarkDescription("", {default_test: 1})
        assert "Benchmark name cannot be empty" in str(excinfo)

        with pytest.raises(EmptyElementException) as excinfo:
            benchmark = BenchmarkDescription("   ", {default_test: 1})
        assert "Benchmark name cannot be empty" in str(excinfo)

    def test_get_name(self):
        assert benchmark_description.name == "Benchmark1"

    def test_get_tests(self):
        assert benchmark_description.tests == [default_test]
        assert benchmark_description.test_occurrences == {default_test: 1}

    def test_to_dict(self):
        test_dict = default_test.to_dict()
        dictionary = {"name": "Benchmark1",
                      "test_occurrences": {"Test1": 1},
                      "tests": [test_dict]}
        print(benchmark_description.to_dict())
        assert benchmark_description.to_dict() == dictionary

    def test_from_dict(self):
        test_dict = default_test.to_dict()
        dictionary = {"name": "Benchmark1",
                      "test_occurrences": {"Test1": 1},
                      "tests": [test_dict]}

        benchmark = BenchmarkDescription.from_dict(dictionary)
        assert benchmark.name == "Benchmark1"
        assert benchmark.tests == [default_test]
        assert benchmark.test_occurrences == {default_test: 1}

