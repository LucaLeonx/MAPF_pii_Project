import csv
import yaml
import datetime

from cli import humanreadable
from cli.humanreadable import MapRepresentation
from formatter import formatter, extractor
from metrics.benchmark_metrics import BenchmarkMetrics
from result.testrun import BenchmarkRun
from runner.benchmarkrunner import BenchmarkRunner


def _setup_yaml():
    yaml.SafeDumper.add_representer(MapRepresentation, MapRepresentation.representer)
    yaml.SafeLoader.add_constructor("!Map", MapRepresentation.constructor)


def load_benchmark(path):
    _setup_yaml()
    with open(path, "r") as bench_file:
        bench_dict = yaml.safe_load(bench_file)
        benchmark_description = extractor.extract_benchmark(bench_dict)

    return benchmark_description


def execute_benchmark(benchmark_runner):
    try:
        benchmark_runner.start_benchmark()
    except KeyboardInterrupt:
        benchmark_runner.stop_benchmark()
    finally:
        return benchmark_runner.get_results()


def export_benchmark_results(benchmark_results, output):
    _setup_yaml()
    with open(output + '.yaml', 'w') as output_file:
        # output_file.write(yaml.dump(benchmark_results.to_dict(), indent=4, sort_keys=False))
        output_file.write(formatter.export_benchmark_results_to_yaml(benchmark_results))


def import_benchmark_results(path):
    _setup_yaml()
    with open(path, "r") as input_file:
        benchmark_results = extractor.extract_benchmark_run(yaml.safe_load(input_file))

    return benchmark_results


def calculate_metrics(benchmark_run: BenchmarkRun):
    elaborated_metrics = BenchmarkMetrics(benchmark_run)
    elaborated_metrics.evaluate()
    return elaborated_metrics


def export_metrics_to_csv(benchmark_metrics, output):
    with open(output + '.csv', 'w', newline='') as csvFile:
        csv_entries = formatter.export_test_iterations_metrics(benchmark_metrics)
        writer = csv.DictWriter(csvFile, csv_entries[0].keys())
        writer.writeheader()
        for entry in csv_entries:
            writer.writerow(entry)

    with open(output + '_aggregate.csv', 'w', newline='') as csvFile:
        csv_entries = formatter.export_aggregate_metrics(benchmark_metrics)
        writer = csv.DictWriter(csvFile, csv_entries[0].keys())
        writer.writeheader()
        for entry in csv_entries:
            writer.writerow(entry)


def prepend_timestamp(string: str):
    return '{date:%Y-%m-%d_%H-%M-%S}_'.format(date=datetime.datetime.now()) + string
