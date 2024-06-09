from jinja2 import Environment, PackageLoader, select_autoescape
from globals import benchmark_description


def main():
    env = Environment(
        loader=PackageLoader("exporter"),
        autoescape=select_autoescape()
    )

    template = env.get_template("benchmark.jinja")

    print(template.render(benchmark=benchmark_description()))


if __name__ == "__main__":
    main()
