import yaml
import pytest

from description.benchmarkdescription import TestDescription
from importer import humanreadable
from importer.humanreadable import MapRepresentation


class TestHumanReadable:

    @pytest.fixture(autouse=True)
    def map_representation(self):
        return MapRepresentation([["T1", "O ", "O", "O", "T2", " "],
                                  ["  ", "  ", "O", "O", "O ", " "],
                                  ["A2", "  ", " ", "O", "  ", " "],
                                  ["  ", "  ", " ", " ", "  ", " "],
                                  ["  ", "A1", " ", " ", "  ", " "]])

    def test_extract_grid_representation(self, map_representation):
        (graph, entities) = humanreadable.extract_grid_information(map_representation)
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
                assert new_representation[x][y].strip() == map_representation[x][y].strip()

    def test_convert_to_humanreadable_dict(self, map_representation):

        yaml.SafeDumper.add_representer(MapRepresentation, MapRepresentation.representer)
        yaml.SafeLoader.add_constructor("!Map", MapRepresentation.constructor)

        (graph, entities) = humanreadable.extract_grid_information(map_representation.representation)
        test_description = TestDescription("GridTest", graph, entities)
        print()
        print(pretty_dump_yaml(test_description))
        test = pretty_dump_yaml(test_description)
        dictionary = yaml.safe_load(test)
        test_again = humanreadable.from_human_readable_dict(dictionary)
        print(test_again.name, test_again.graph.rows, test_again.graph.cols)
        print(dictionary)


def pretty_dump_yaml(test):
    text = yaml.safe_dump(humanreadable.to_human_readable_dict(test),
                          indent=4,
                          sort_keys=False)
    return text
