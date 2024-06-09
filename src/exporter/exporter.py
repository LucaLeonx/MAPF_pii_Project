import yaml
from jinja2 import Environment, PackageLoader, select_autoescape

from cli import humanreadable
from cli.humanreadable import MapRepresentation


def export_benchmark(benchmark):
    env = Environment(
        loader=PackageLoader("exporter"),
        autoescape=select_autoescape()
    )

    env.globals["MapRepresentation"] = MapRepresentation
    template = env.get_template("benchmark.jinja")

    return template.render(benchmark=benchmark)


def main():
    yaml.SafeDumper.add_representer(MapRepresentation, MapRepresentation.representer)
    yaml.SafeLoader.add_constructor("!Map", MapRepresentation.constructor)

    with open("../../docs/examples/multi_iteration_benchmark.yaml", "r") as bench_file:
        bench_dict = yaml.safe_load(bench_file)
        benchmark_description = humanreadable.convert_from_human_readable_dict(bench_dict)
        print(export_benchmark(benchmark_description))


if __name__ == "__main__":
    main()
