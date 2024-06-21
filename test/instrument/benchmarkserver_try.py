import asyncio
from pathlib import Path
from time import sleep

# import pytest

from mapfbench.importer import import_scenarios
from mapfbench.instrument.server import BenchmarkServer


def start_server():

    scenarios = import_scenarios(str(Path(__file__).parent.parent / 'importer' / 'map_files' / 'arena.map.scen'))
    server = BenchmarkServer(scenarios[1:], "tcp://localhost:9365")

    try:
        print("Server started")
        server.start()
        while True:
            sleep(1)
            # print(server.status)  # Show assigned scenarios, number of iterations, completed
            if not server.status["Running"]:
                break
    except KeyboardInterrupt:
        print("Server stopped")
        server.stop()  # Stop the server

    print(server.plans)


if __name__ == '__main__':
    start_server()
