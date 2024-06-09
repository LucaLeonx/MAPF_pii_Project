import yaml
from jinja2 import Environment, PackageLoader, select_autoescape

from cli import humanreadable
from cli.humanreadable import MapRepresentation
import globals


def export_benchmark_to_yaml(benchmark):
    env = Environment(
        loader=PackageLoader("formatter"),
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True
    )

    env.globals["MapRepresentation"] = MapRepresentation
    template = env.get_template("benchmark.jinja")

    return template.render(benchmark=benchmark)


def export_benchmark_run_to_yaml(benchmark_run):
    env = Environment(
        loader=PackageLoader("formatter"),
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True
    )

    env.globals["MapRepresentation"] = MapRepresentation
    template = env.get_template("results.jinja")

    return template.render(benchmark=benchmark_run)


def export_test_iterations_metrics(benchmark_metrics):
    lines = []
    for aggregate_metric in benchmark_metrics.aggregate_metrics:
        for index, test_metric in enumerate(aggregate_metric.iterations_metrics):
            line = ({"Test name": aggregate_metric.test_name,
                     "Iteration": index + 1})
            line.update(test_metric.to_dict())
            del line["Collisions"]
            del line["TestRun"]
            lines.append(line)

    return lines


def export_aggregate_metrics(benchmark_metrics):
    lines = []
    for aggregate_metric in benchmark_metrics.aggregate_metrics:
        lines.append(aggregate_metric.to_dict())

    return lines


def main():
    yaml.SafeDumper.add_representer(MapRepresentation, MapRepresentation.representer)
    yaml.SafeLoader.add_constructor("!Map", MapRepresentation.constructor)

    # with open("../../docs/examples/multi_iteration_benchmark.yaml", "r") as bench_file:
    #    bench_dict = yaml.safe_load(bench_file)
    #    benchmark_description = humanreadable.convert_from_human_readable_dict(bench_dict)
    #    print(export_benchmark_to_yaml(benchmark_description))

    print(export_benchmark_run_to_yaml(globals.benchmark_run()))


if __name__ == "__main__":
    main()
