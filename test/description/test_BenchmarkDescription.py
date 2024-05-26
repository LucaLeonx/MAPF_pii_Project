import pytest

from description.benchmarkdescription import BenchmarkDescription, TestDescription
from description.entity_description import AgentDescription, ObstacleDescription, ObjectiveDescription
from description.map.graph import Node, Edge, Graph
from exceptions import EmptyElementException


class TestBenchmarkDescription:
    @pytest.fixture
    def entity_list(self):
        objective1 = ObjectiveDescription("T1")
        objective2 = ObjectiveDescription("T2")
        objective3 = ObjectiveDescription("T3")

        agent1 = AgentDescription("A1", "T1", start_position=Node(1))
        agent2 = AgentDescription("A2", "T2", start_position=Node(2))
        agent3 = AgentDescription("A3", "T3", start_position=Node(3))

        obstacle = ObstacleDescription("O1")

        return [objective1, objective2, objective3, agent1, agent2, agent3, obstacle]

    @pytest.fixture
    def graph(self):
        return Graph(edge_list=[Edge(Node(1), Node(2)),
                                Edge(Node(1), Node(3)),
                                Edge(Node(2), Node(3)),
                                Edge(Node(3), Node(2)),
                                Edge(Node(3), Node(4))
                                ])

    @pytest.fixture
    def test_description(self, graph, entity_list):
        return TestDescription("Test1", graph, entity_list)

    # Useful if more than one test must be generated
    @pytest.fixture
    def default_test(self, test_description):
        return test_description

    @pytest.fixture
    def benchmark_description(self, default_test):
        return BenchmarkDescription("Benchmark1", [default_test], "Example benchmark",)

    @pytest.fixture
    def empty_benchmark(self, default_test):
        return BenchmarkDescription("Empty", [default_test])

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
