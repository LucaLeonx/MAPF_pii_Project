#!/usr/bin/python3
import yaml

import globals
from cli import commands
from importer import humanreadable
from importer.humanreadable import MapRepresentation
from result.testrun import TestRun
from metrics.testMetrics import TestMetrics


# Main file of MAPF Benchmark

def main():
    yaml.SafeDumper.add_representer(MapRepresentation, MapRepresentation.representer)
    yaml.SafeLoader.add_constructor("!Map", MapRepresentation.constructor)
    print("Hello, MAPF Benchmark!")
    benchmark_description = None
    with open("sample_benchmark.yaml", "r") as bench_file:
        bench_dict = yaml.safe_load(bench_file)
        benchmark_description = humanreadable.convert_from_human_readable_dict(bench_dict)

    results = commands.execute_benchmark(benchmark_description)
    print(results)
    result_list = []
    for result in results.values():
        for test_result in result:
            result_list.append(test_result.to_dict())

    # metrics = TestMetrics(results["GridTest"][0])
    # metrics.run()

    with open("results.yaml", "w") as results_file:
        results_file.write(yaml.dump(result_list, indent=4, sort_keys=False))


def test_run():
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
                                   'end_position': {'index': 2}, 'description': 'Move'},
                                  {'type': 'MoveAction', 'timestep': 1, 'subject': 'A2', 'start_position': {'index': 2},
                                   'end_position': {'index': 1}, 'description': 'Move'},
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


if __name__ == "__main__":
    main()
