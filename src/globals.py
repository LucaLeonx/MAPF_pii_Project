from description.benchmarkdescription import TestDescription, BenchmarkDescription
from description.entity_description import ObstacleDescription, AgentDescription, ObjectiveDescription
from description.map.graph import Node, Edge, Graph
from result.testrun import TestRun, BenchmarkRun


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
    return Graph([Edge(Node(1), Node(2)),
                  Edge(Node(1), Node(3)),
                  Edge(Node(2), Node(3)),
                  Edge(Node(3), Node(2)),
                  Edge(Node(3), Node(4))
                  ])


def generate_default_test(test_name: str) -> TestDescription:
    return TestDescription(test_name, graph(), entity_list())


def test_description() -> TestDescription:
    return generate_default_test("Test1")


def test_run() -> TestRun:
    return TestRun.from_dict({'test_description':
                                  {'name': 'Test1',
                                   'graph': {'type': 'Graph',
                                             'edges': [
                                                 {'start_node': {'index': 1}, 'end_node': {'index': 2}, 'weight': 1},
                                                 {'start_node': {'index': 3}, 'end_node': {'index': 4}, 'weight': 1},
                                                 {'start_node': {'index': 2}, 'end_node': {'index': 3}, 'weight': 1},
                                                 {'start_node': {'index': 3}, 'end_node': {'index': 2}, 'weight': 1},
                                                 {'start_node': {'index': 1}, 'end_node': {'index': 3}, 'weight': 1}]},
                                   'entities': [{'type': 'ObjectiveDescription', 'name': 'T1'},
                                                {'type': 'ObjectiveDescription', 'name': 'T2'},
                                                {'type': 'ObjectiveDescription', 'name': 'T3'},
                                                {'type': 'AgentDescription', 'name': 'A1',
                                                 'start_position': {'index': 1}, 'objective': 'T1'},
                                                {'type': 'AgentDescription', 'name': 'A2',
                                                 'start_position': {'index': 2}, 'objective': 'T2'},
                                                {'type': 'AgentDescription', 'name': 'A3',
                                                 'start_position': {'index': 3}, 'objective': 'T3'},
                                                {'type': 'ObstacleDescription', 'name': 'O1'}]},
                              'action_list': [
                                  {'type': 'AppearAction', 'timestep': 0, 'subject': 'A1', 'end_position': {'index': 1},
                                   'description': 'Appear'},
                                  {'type': 'AppearAction', 'timestep': 0, 'subject': 'A2', 'end_position': {'index': 2},
                                   'description': 'Appear'},
                                  {'type': 'AppearAction', 'timestep': 0, 'subject': 'A3', 'end_position': {'index': 3},
                                   'description': 'Appear'},
                                  {'type': 'MoveAction', 'timestep': 1, 'subject': 'A1', 'start_position': {'index': 1},
                                   'end_position': {'index': 1}, 'description': 'Move'},
                                  {'type': 'MoveAction', 'timestep': 1, 'subject': 'A2', 'start_position': {'index': 2},
                                   'end_position': {'index': 3}, 'description': 'Move'},
                                  {'type': 'MoveAction', 'timestep': 1, 'subject': 'A3', 'start_position': {'index': 3},
                                   'end_position': {'index': 4}, 'description': 'Move'},
                                  {'type': 'WaitAction', 'timestep': 2, 'subject': 'A2', 'start_position': {'index': 3},
                                   'description': 'Wait'},
                                  {'type': 'DisappearAction', 'timestep': 2, 'subject': 'A1',
                                   'description': 'Disappear'},
                                  {'type': 'AppearAction', 'timestep': 3, 'subject': 'T3',
                                   'end_position': {'index': 12}, 'description': 'Appear'},
                                  {'type': 'MoveAction', 'timestep': 4, 'subject': 'T3',
                                   'start_position': {'index': 12}, 'end_position': {'index': 8},
                                   'description': 'MoveLeft'},
                                  {'type': 'MoveAction', 'timestep': 5, 'subject': 'T3', 'start_position': {'index': 8},
                                   'end_position': {'index': 13}, 'description': 'MoveUp'}],
                              'is_solved': False})


def benchmark_description():
    return BenchmarkDescription("Benchmark1", {test_description(): 1})


def empty_benchmark():
    return BenchmarkDescription("Empty", {test_description(): 1})


def benchmark_run():
    return BenchmarkRun(benchmark_description(), {"Test1": [test_run()]})