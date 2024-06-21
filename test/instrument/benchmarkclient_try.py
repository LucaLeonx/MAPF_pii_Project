import asyncio

from mapfbench.instrument.server import BenchmarkClient, TestsFinishedException


def start_client():
    client = BenchmarkClient(connection_address="tcp://localhost:9365")
    client.start()
    try:
        while True:
            recorder = client.request_scenario()
            recorder.record_move(1, 1, end_position=[10, 10])
            client.submit_plan(recorder)
            i += 1
    except TestsFinishedException:
        print("Test finished successfully")
    finally:
        client.stop()


if __name__ == "__main__":
    start_client()

    # Or

    #pool = BenchmarkExecutionPool(scenarios, solver_function, timeout)
    #results = pool.start()  # Non blocking
    #pool.get_status()
    #pool.abort()  # if something goes wrong
    #results.get()  # To obtain results