import asyncio
from pathlib import Path
from time import sleep

from mapfbench.exporter import export_plans, export_results_to_csv
# import pytest

from mapfbench.importer import import_scenarios
from mapfbench.instrument.server import BenchmarkServer
from mapfbench.metrics import AggregatePlanResults


def start_server():

    scenarios = import_scenarios(str(Path(__file__).parent.parent / 'importer' / 'map_files' / 'arena.map.scen'))
    server = BenchmarkServer(scenarios[:6])

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
        return

    print("Tests completed, exporting results...")
    results = AggregatePlanResults(server.plans)
    results.evaluate()
    export_plans(results, "plans")
    export_results_to_csv(results, "metrics")


if __name__ == '__main__':
    start_server()
