import click
from cli.cli_commands import *


@click.group()
def mapfbench():
    pass


# TODO: use proper click callbacks for this command

@mapfbench.command("run")
@click.argument('path', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
@click.option('-oi', '--output-iterations', 'output_iterations', type=str)
@click.option('-om', '--output-metrics', 'output_metrics', type=str)
def collect_data(path, output_iterations="", output_metrics=""):
    benchmark_description = None
    benchmark_result = None
    partial_result = None
    try:
        benchmark_description = load_benchmark(path)
    except Exception as e:
        click.echo(e)

    try:
        click.echo("Benchmark running...")
        partial_result = execute_benchmark(benchmark_description)
    except KeyboardInterrupt:
        click.echo("Benchmark interrupted by user")
    except Exception as e:
        click.echo(e)
    finally:
        benchmark_result = partial_result

    click.echo("Benchmark finished, writing results to file")
    if not output_iterations:
        output_iterations = prepend_timestamp(benchmark_description.name.replace(" ", "_")) + ".yaml"

    export_benchmark_results(benchmark_result, output_iterations)
    click.echo(f"Results written to: {output_iterations}")

    if not output_metrics:
        output_metrics = prepend_timestamp(benchmark_result.name.replace(" ", "_")) + ".csv"

    click.echo("Calculating metrics...")
    metrics = calculate_metrics(benchmark_result)
    export_metrics_to_csv(metrics, output_metrics)
    click.echo(f"Calculated indices written to: {output_metrics}")


@mapfbench.command("collect")
@click.argument('path', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
@click.option('-o', '--output', 'output', type=str)
def collect_data(path, output=""):
    benchmark_description = None
    benchmark_result = None
    partial_result = None
    try:
        benchmark_description = load_benchmark(path)
    except Exception as e:
        click.echo(e)

    try:
        click.echo("Benchmark running...")
        partial_result = execute_benchmark(benchmark_description)
    except KeyboardInterrupt:
        click.echo("Benchmark interrupted by user")
    except Exception as e:
        click.echo(e)
    finally:
        benchmark_result = partial_result

    click.echo("Benchmark finished, writing results to file")
    if not output:
        output = prepend_timestamp(benchmark_description.name.replace(" ", "_")) + ".yaml"

    export_benchmark_results(benchmark_result, output)
    click.echo(f"Results written to: {output}")


@mapfbench.command("measure")
@click.argument('path', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
@click.option('-o', '--output', 'output', type=str)
def measure_metrics(path: str, output=None):
    benchmark_results = None
    try:
        benchmark_results = import_benchmark_results(path)
    except Exception as e:
        click.echo(e)

    if not output:
        output = prepend_timestamp(benchmark_results.name.replace(" ", "_")) + ".csv"

    click.echo("Calculating metrics...")
    metrics = calculate_metrics(benchmark_results)
    export_metrics_to_csv(metrics, output)
    click.echo(f"Calculated indices written to: {output}")


def _prepend_timestamp(string: str):
    return '{date:%Y-%m-%d_%H:%M:%S}_'.format(date=datetime.datetime.now()) + string
