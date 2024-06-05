import csv
import yaml
import datetime

from cli import humanreadable
from cli.humanreadable import MapRepresentation
from metrics.testMetrics import TestMetrics
from result.testrun import BenchmarkRun
from runner.benchmarkrunner import BenchmarkRunner


def _setup_yaml():
    yaml.SafeDumper.add_representer(MapRepresentation, MapRepresentation.representer)
    yaml.SafeLoader.add_constructor("!Map", MapRepresentation.constructor)


def load_benchmark(path):
    _setup_yaml()
    with open(path, "r") as bench_file:
        bench_dict = yaml.safe_load(bench_file)
        benchmark_description = humanreadable.convert_from_human_readable_dict(bench_dict)

    return benchmark_description


def execute_benchmark(benchmark_description):
    benchmark_runner = BenchmarkRunner(benchmark_description)

    try:
        benchmark_runner.start_benchmark()
    except KeyboardInterrupt:
        benchmark_runner.stop_benchmark()
    finally:
        return benchmark_runner.get_results()


def export_benchmark_results(benchmark_results, output):
    _setup_yaml()
    with open(output, 'w') as output_file:
        output_file.write(yaml.dump(benchmark_results.to_dict(), indent=4, sort_keys=False))


def import_benchmark_results(path):
    _setup_yaml()
    with open(path, "r") as input_file:
        benchmark_results = BenchmarkRun.from_dict(yaml.safe_load(input_file))

    return benchmark_results


def calculate_metrics(benchmark_run: BenchmarkRun):
    metrics = []
    for test_run in benchmark_run.result_list:
        metric = TestMetrics(test_run)
        metric.run()
        metrics.append(metric)

    return metrics


def export_metrics_to_csv(metrics, output):

    # Taken from Exporter class code

    csv_entries = [metric.to_dict() for metric in metrics]

    if csv_entries:
        with open(output, 'w', newline='') as csvFile:
            writer = csv.DictWriter(csvFile, csv_entries[0].keys())
            writer.writeheader()
            for entry in csv_entries:
                writer.writerow(entry)


def prepend_timestamp(string: str):
    return '{date:%Y-%m-%d_%H-%M-%S}_'.format(date=datetime.datetime.now()) + string
