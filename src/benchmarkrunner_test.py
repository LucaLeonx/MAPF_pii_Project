import sys

import yaml

import globals
from cli import cli_commands
from description.benchmarkdescription import BenchmarkDescription
from runner.benchmarkrunner import BenchmarkRunner
from connection.connectionconfig import TCPConnectionConfig
from result.testrun import TestRun

import json
# import globals

# benchmark_description = globals.benchmark_description()

from description.benchmarkdescription import TestDescription, BenchmarkDescription
from description.entity_description import ObstacleDescription, AgentDescription, ObjectiveDescription
from description.map.graph import Node, Edge, Graph

if __name__ == '__main__':
    benchmark_description = BenchmarkDescription("Benchmark", {globals.generate_default_test("Test1"): 2,
                                                               globals.generate_default_test("Test2"): 1})
    runner = BenchmarkRunner(benchmark_description)
    runner.start_benchmark()

    results = runner.get_results()

    print(results)
    for result_list in results.values():
        for result in result_list:
            string = yaml.dump(result.to_dict(), indent=4, sort_keys=False)

    print("Saving results done")

    sys.exit()

