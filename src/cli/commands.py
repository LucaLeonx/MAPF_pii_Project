import asyncio
from asyncio import Event, CancelledError
from concurrent.futures import ThreadPoolExecutor

from description.benchmarkdescription import BenchmarkDescription
from runner.benchmarkrunner import BenchmarkRunner


async def run_benchmark(runner: BenchmarkRunner):
    runner.start_benchmark()


def execute_benchmark(benchmark: BenchmarkDescription):
    benchmark_runner = BenchmarkRunner(benchmark)

    try:
        benchmark_runner.start_benchmark()
    except KeyboardInterrupt:
        print("Benchmark Interrupted by user")
        benchmark_runner.stop_benchmark()
    finally:
        return benchmark_runner.get_results()
