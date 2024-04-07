import pytest

from benchmark.benchmarkdescription import BenchmarkDescription
from benchmark.testdescription import TestDescription
from entity.agent_description import AgentDescription
from entity.objective_description import ObjectiveDescription
from entity.obstacle_description import ObstacleDescription
from graph.edge import Edge
from graph.graph import Graph
from graph.node import Node
from test_TestDescription import TestTestDescription


class TestBenchmarkDescription:
    @pytest.fixture
    def entity_list(self):
        objective1 = ObjectiveDescription("T1")
        objective2 = ObjectiveDescription("T2")
        objective3 = ObjectiveDescription("T3")

        agent1 = AgentDescription("A1", start_position=Node(1), objective=objective1)
        agent2 = AgentDescription("A2", start_position=Node(2), objective=objective2)
        agent3 = AgentDescription("A3", start_position=Node(3), objective=objective3)

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
        return BenchmarkDescription("Benchmark1", "Example benchmark", [default_test])

    @pytest.fixture
    def empty_benchmark(self):
        return BenchmarkDescription("Empty")

    def test_init_guards(self):
        with pytest.raises(ValueError) as excinfo:
            benchmark = BenchmarkDescription("")
        assert "Benchmark name cannot be empty" in str(excinfo)

    def test_get_name(self, benchmark_description):
        assert benchmark_description.get_name() == "Benchmark1"

    def test_get_description(self, benchmark_description, empty_benchmark):
        assert benchmark_description.get_description() == "Example benchmark"
        assert empty_benchmark.get_description() == ""

    def test_get_tests(self, benchmark_description, empty_benchmark, default_test):
        assert benchmark_description.get_tests() == [default_test]
        assert empty_benchmark.get_tests() == []
