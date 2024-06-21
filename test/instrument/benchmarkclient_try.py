import asyncio

from mapfbench.instrument.server import BenchmarkClient, TestsFinishedException


def start_client():
    client = BenchmarkClient(connection_address="tcp://localhost:9362")
    client.start()
    try:
        while True:
            recorder = asyncio.run(client.request_scenario())
            recorder.record_move(1, 1, end_position=[10, 10])
    except TestsFinishedException:
        print("Test finished successfully")


if __name__ == "__main__":
    start_client()

    # Or

    #pool = BenchmarkExecutionPool(scenarios, solver_function, timeout)
    #results = pool.start()  # Non blocking
    #pool.get_status()
    #pool.abort()  # if something goes wrong
    #results.get()  # To obtain results