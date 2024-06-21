import argparse
from time import sleep

from mapfbench.exporter import export_plans, export_results_to_csv
from mapfbench.importer import import_scenarios
from mapfbench.instrument.server import BenchmarkServer
from mapfbench.metrics import AggregatePlanResults


def cli():
    parser = argparse.ArgumentParser(
        prog='mapfbench-run',
        description='Run a benchmark server')

    parser.add_argument("filename", help="Filename of the scenario files to run")
    parser.add_argument("output", help="Filename of the output files")
    parser.add_argument("-A", "--address", help="IP address of the server", default="localhost")
    parser.add_argument("-P", "--port", help="Port of the server", type=int, default=9361)
    args = parser.parse_args()
    mapfbench_run(args)


def mapfbench_run(args):
    address = "tcp://{}:{}".format(args.address, args.port)

    scenarios = import_scenarios(args.filename)
    server = BenchmarkServer(scenarios)

    try:
        print("Server started")
        server.start()
        while True:
            sleep(2)
            if not server.status["Running"]:
                break
    except KeyboardInterrupt:
        print("Server stopped")
        server.stop()  # Stop the server
        return

    print("Tests completed, calculating and exporting results...")
    results = AggregatePlanResults(server.plans)
    results.evaluate()
    export_plans(results, args.output + "_plans")
    export_results_to_csv(results, args.output + "_metrics")
