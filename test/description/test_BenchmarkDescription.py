import pytest

from description.benchmarkdescription import BenchmarkDescription, TestDescription
from description.entity_description import AgentDescription, ObstacleDescription, ObjectiveDescription
from description.map.graph import Node, Edge, Graph
from exceptions import EmptyElementException


class TestBenchmarkDescription:


    def test_init_guards(self, default_test):
        with pytest.raises(EmptyElementException) as excinfo:
            benchmark = BenchmarkDescription("No-tests", [])
        assert "Benchmark must have at least one test" in str(excinfo)

        with pytest.raises(EmptyElementException) as excinfo:
            benchmark = BenchmarkDescription("", [default_test])
        assert "Benchmark name cannot be empty" in str(excinfo)

        with pytest.raises(EmptyElementException) as excinfo:
            benchmark = BenchmarkDescription("   ", [default_test])
        assert "Benchmark name cannot be empty" in str(excinfo)

    def test_get_name(self, benchmark_description):
        assert benchmark_description.name == "Benchmark1"

    def test_get_description(self, benchmark_description, empty_benchmark):
        assert benchmark_description.description == "Example benchmark"
        assert empty_benchmark.description == ""

    def test_get_tests(self, benchmark_description, empty_benchmark, default_test):
        assert benchmark_description.tests == [default_test]
