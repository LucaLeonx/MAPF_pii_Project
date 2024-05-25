from benchmark.benchmarkdescription import BenchmarkDescription
from benchmark.testdescription import TestDescription
from connection.tcpconnectionconfig import TCPConnectionConfig
from entity.agent_description import AgentDescription
from entity.objective_description import ObjectiveDescription
from entity.obstacle_description import ObstacleDescription
from graph.edge import Edge
from graph.graph import Graph
from graph.node import Node
from runner.benchmarkrunner import BenchmarkRunner


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


def description_of_test():
    return TestDescription("Test1", graph(), entity_list())


def benchmark_description():
    return BenchmarkDescription("Benchmark1", "Example benchmark", [description_of_test()])


if __name__ == '__main__':
    benchmark_runner = BenchmarkRunner(benchmark_description(), TCPConnectionConfig("localhost", 9361))
    print("Starting...")
    benchmark_runner.run_benchmark()
    print("Finished")
    print(benchmark_runner.get_results())
