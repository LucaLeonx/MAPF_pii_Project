import json

import pytest

from benchmark.benchmarkdescription import BenchmarkDescription
from benchmark.testdescription import TestDescription
from entity.agent_description import AgentDescription
from entity.objective_description import ObjectiveDescription
from entity.obstacle_description import ObstacleDescription
from graph.edge import Edge
from graph.graph import Graph
from graph.node import Node


class TestJSONEncoders(object):

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
                                Edge(Node(1), Node(3), weight=15),
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

    def test_json_encoders(self, benchmark_description):
        assert json.dumps(Node(1).to_dict()) == '{"index": 1}'
        assert (json.dumps(Edge(Node(2),
                                Node(3),
                                weight=31).to_dict()) ==
                '{"start_node": {"index": 2}, "end_node": {"index": 3}, "weight": 31}')

        jsonstr = json.dumps(Edge(Node(2),
                                Node(3),
                                weight=31).to_dict(use_coordinates=True))
        json_dict = json.loads(jsonstr)

        #print(json_dict)

        edge = Edge.from_dict(json_dict, use_coordinates=True)
        #print(edge)

        benchmark_description_json = json.dumps(benchmark_description.to_dict())
        #print(benchmark_description_json)
        benchmark_description_restored = BenchmarkDescription.from_dict(json.loads(benchmark_description_json))
        print("\n" + str(benchmark_description_restored))


        #print(json.dumps(AgentDescription("A","B", Node(10)).to_dict()))
        #print(json.loads(json.dumps(benchmark_description.to_dict())))


