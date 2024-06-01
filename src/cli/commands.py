from asyncio import Event
from concurrent.futures import ThreadPoolExecutor

from description.benchmarkdescription import BenchmarkDescription
from runner.benchmarkrunner import BenchmarkRunner


def run_benchmark(benchmark: BenchmarkDescription):
    runner = BenchmarkRunner(benchmark)
    executor = ThreadPoolExecutor(max_workers=1)
    stop_event = Event()
    print("Server started")

    result = executor.submit(runner.run_benchmark)

    try:
        while not result.done():
            print("Waiting for results from inspectors...")
    except KeyboardInterrupt:
        print("Server interrupted by user")
        # stop_event.set()
        runner.stop_benchmark()
        executor.shutdown(wait=False, cancel_futures=True)
    finally:
        print("Finishing...")
        runner.stop_benchmark()
        return runner.get_results()

