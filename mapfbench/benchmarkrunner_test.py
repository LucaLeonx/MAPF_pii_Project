import sys

import yaml

import globals
from description.benchmarkdescription import BenchmarkDescription
from runner.benchmarkrunner import BenchmarkRunner

# import globals
# benchmark_description = globals.benchmark_description()

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

