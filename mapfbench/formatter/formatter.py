from jinja2 import Environment, PackageLoader, select_autoescape
from formatter.maprepresentation import MapRepresentation


def _setup_environment():
    env = Environment(
        loader=PackageLoader("formatter"),
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=False
    )

    env.globals["MapRepresentation"] = MapRepresentation
    return env


def export_benchmark_to_yaml(benchmark):
    env = _setup_environment()
    template = env.get_template("benchmark.jinja")
    return template.render(benchmark=benchmark)


def export_benchmark_run_to_yaml(benchmark_run):
    env = _setup_environment()
    template = env.get_template("benchmark_run.jinja")
    return template.render(benchmark=benchmark_run)


def export_benchmark_results_to_yaml(benchmark_results):
    env = _setup_environment()
    template = env.get_template("benchmark_results.jinja")
    return template.render(benchmark=benchmark_results)


def export_test_iterations_metrics(benchmark_metrics):
    lines = []
    for aggregate_metric in benchmark_metrics.aggregate_metrics:
        for index, test_metric in enumerate(aggregate_metric.iterations_metrics):
            line = ({"Test name": aggregate_metric.test_name,
                     "Iteration": index + 1})
            line.update(test_metric.to_dict())
            del line["Collisions"]
            del line["TestName"]
            del line["TestRun"]
            lines.append(line)

    return lines


def export_aggregate_metrics(benchmark_metrics):
    lines = []
    for aggregate_metric in benchmark_metrics.aggregate_metrics:
        lines.append(aggregate_metric.to_dict())

    return lines
