from description.benchmarkdescription import BenchmarkDescription
from runner.benchmarkrunner import BenchmarkRunner
from connection.connectionconfig import TCPConnectionConfig
import json
# import globals

# benchmark_description = globals.benchmark_description()

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
    return Graph([Edge(Node(1), Node(2)),
                  Edge(Node(1), Node(3)),
                  Edge(Node(2), Node(3)),
                  Edge(Node(3), Node(2)),
                  Edge(Node(3), Node(4))
                  ])


def description():
    return TestDescription("Test1", graph(), entity_list())


def benchmark_description():
    return BenchmarkDescription("Benchmark1", {description(): 1})


def empty_benchmark():
    return BenchmarkDescription("Empty", {description(): 1})


if __name__ == '__main__':
    benchmark_runner = BenchmarkRunner(benchmark_description(), TCPConnectionConfig("localhost", 9361))
    print("Starting...")
    benchmark_runner.run_benchmark()
    print("Finished")
    results = benchmark_runner.get_results()

    for result_list in results:
        for result in result_list:
            print(json.dumps(result.to_dict(), indent=4))
