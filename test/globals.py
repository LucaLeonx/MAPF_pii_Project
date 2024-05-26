from description.benchmarkdescription import TestDescription, BenchmarkDescription
from description.entity_description import ObstacleDescription, AgentDescription, ObjectiveDescription
from description.map.graph import Node, Edge, Graph


def entity_list():
    objective1 = ObjectiveDescription("T1")
    objective2 = ObjectiveDescription("T2")
    objective3 = ObjectiveDescription("T3")

    agent1 = AgentDescription("A1", "T1", start_position=Node(1))
    agent2 = AgentDescription("A2", "T2", start_position=Node(2))
    agent3 = AgentDescription("A3", "T3", start_position=Node(3))

    obstacle = ObstacleDescription("O1")

    return [objective1, objective2, objective3, agent1, agent2, agent3, obstacle]


def graph():
    return Graph(edge_list=[Edge(Node(1), Node(2)),
                            Edge(Node(1), Node(3)),
                            Edge(Node(2), Node(3)),
                            Edge(Node(3), Node(2)),
                            Edge(Node(3), Node(4))
                            ])


def test_description():
    return TestDescription("Test1", graph(), entity_list())


def benchmark_description():
    return BenchmarkDescription("Benchmark1", [test_description()], "Example benchmark", )


def empty_benchmark():
    return BenchmarkDescription("Empty", [test_description()])
