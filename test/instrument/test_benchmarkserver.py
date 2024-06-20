import pytest


class TestBenchmarkServer:

    def start_server(self):

        scenarios = import_scenarios(self, filename)
        server = BenchmarkServer(scenarios, connection_config = ...)
        server.start()
        server.abort() # if something goes wrong
        server.get_status() # Show assigned scenarios, number of iterations, completed
        results = server.results()   # Return async wait for results
        server.stop() # Stop the server

    def start_client(self):

        client = BenchmarkClient()
        client.start()
        try:
            client.request_test() # Returns a test; throws an exception if a test is not available

        # Or

        pool = BenchmarkExecutionPool(scenarios, solver_function, timeout)
        results = pool.start() # Non blocking
        pool.get_status()
        pool.abort() # if something goes wrong
        results.get() # To obtain results