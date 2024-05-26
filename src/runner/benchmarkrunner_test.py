from description.benchmarkdescription import BenchmarkDescription
from runner.benchmarkrunner import BenchmarkRunner
from connection.connectionconfig import TCPConnectionConfig

import globals

benchmark_description = globals.benchmark_description()

if __name__ == '__main__':
    benchmark_runner = BenchmarkRunner(benchmark_description, TCPConnectionConfig("localhost", 9361))
    print("Starting...")
    benchmark_runner.run_benchmark()
    print("Finished")
    print(benchmark_runner.get_results())
