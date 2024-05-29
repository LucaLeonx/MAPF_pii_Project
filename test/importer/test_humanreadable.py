import yaml
import pytest

from description.benchmarkdescription import TestDescription
from importer import humanreadable


class MapRepresentation:
    def __init__(self, representation):
        self._representation = representation

    @property
    def representation(self):
        return self._representation

    @property
    def rows(self):
        return len(self._representation)

    @property
    def cols(self):
        return len(self._representation[0])

    def pretty_print(self):
        print()
        print('{0: <3}|'.format(" "), end="")
        for i in range(self.cols):
            print('{0: <3}|'.format(i), end="")
        print()

        for i, line in enumerate(self.representation):
            print('{0: <3}|'.format(i), end="")
            for cell in line:
                print('{0: <3}|'.format(cell.strip()), end="")
            print()

    @staticmethod
    def represent_map(dumper, data):
        serializedData = "|\n"
        for line in data:
            serializedData += str(line) + "\n"

        return dumper.represent_mapping('!MapRepresentation', serializedData)


yaml.add_constructor("!MapRepresentation", MapRepresentation.represent_map)

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
        (graph, entities) = humanreadable.extract_grid_information(map_representation.representation)
        test_description = TestDescription("GridTest", graph, entities)
        print()
        print(pretty_print_yaml(test_description))


def pretty_print_yaml(test):
    text = yaml.dump(humanreadable.to_human_readable_dict(test), line_break=",",
                     indent=4,
                     sort_keys=False)
    text.replace("]", "]\n")
    return text


