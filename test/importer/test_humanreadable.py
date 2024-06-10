import yaml
import pytest

import formatter.formatter
import globals
from description.benchmarkdescription import TestDescription, BenchmarkDescription
from description.map.graph import GridGraph
from cli import humanreadable
from cli.humanreadable import MapRepresentation
from formatter import extractor


class TestHumanReadable:

    @pytest.fixture(autouse=True)
    def map_representation(self):
        return MapRepresentation([["T1", "O ", "O", "O", "T2", " "],
                                  ["  ", "  ", "O", "O", "O ", " "],
                                  ["A2", "  ", " ", "O", "  ", " "],
                                  ["  ", "  ", " ", " ", "  ", " "],
                                  ["  ", "A1", " ", " ", "  ", " "]])

    def test_extract_grid_representation(self, map_representation):
        (graph, entities) = humanreadable.extract_grid_information(map_representation.representation)
        edges = graph.edges

        for entity in entities:
            print(entity)

        map_representation.pretty_print()

    def test_convert_to_grid_representation(self, map_representation):
        (graph, entities) = humanreadable.extract_grid_information(map_representation.representation)
        new_representation = humanreadable._generate_grid_representation(graph.rows, graph.cols, entities)
        map_representation.pretty_print()

        for x in range(len(new_representation)):
            for y in range(len(new_representation[0])):
                assert new_representation[x][y].strip() == map_representation.representation[x][y].strip()

    def test_convert_to_humanreadable_dict(self, map_representation):

        yaml.SafeDumper.add_representer(MapRepresentation, MapRepresentation.representer)
        yaml.SafeLoader.add_constructor("!Map", MapRepresentation.constructor)

        test_description = TestDescription("GridTest", GridGraph(map_representation.rows,
                                                                 map_representation.cols),
                                           map_representation.entities)
        print(pretty_dump_yaml(test_description))
        test = pretty_dump_yaml(test_description)
        dictionary = yaml.safe_load(test)
        test_again = humanreadable.from_human_readable_dict(dictionary)
        print(test_again.name, test_again.graph.rows, test_again.graph.cols)
        print(test_again.to_dict())
        benchmark = BenchmarkDescription("Benchmark_Example", {test_again: 2})
        with open("benchmark.yaml", "w") as file:
            file.write(yaml.safe_dump(humanreadable.convert_to_human_readable_dict(benchmark), indent=4,
                                      sort_keys=False))


def pretty_dump_yaml(test):
    text = yaml.safe_dump(humanreadable.to_human_readable_dict(test),
                          indent=4,
                          sort_keys=False)
    return text


def test_import():
    yaml.SafeDumper.add_representer(MapRepresentation, MapRepresentation.representer)
    yaml.SafeLoader.add_constructor("!Map", MapRepresentation.constructor)

    with open("X:\MAPF_pii_Project\src\\2024-06-10_10-14-19_MultiIterationBenchmark.yaml", "r") as file:
        dictionary = yaml.safe_load(file)
        benchmark_run = extractor.extract_benchmark_run(dictionary)

        print(benchmark_run.result_list[0].action_list[0])

    # dictionary = yaml.safe_load(formatter.formatter.export_benchmark_to_yaml(globals.benchmark_description()))
    # benchmark_description = extractor.extract_benchmark(dictionary)
    # print(benchmark_description.name)
    # print(benchmark_description.tests[0].graph)

