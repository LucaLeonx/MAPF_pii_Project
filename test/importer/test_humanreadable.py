import pytest
from importer import humanreadable


def pretty_print_map(map_repr):
    print()
    print('{0: <3}|'.format(" "), end="")
    for i in range(len(map_repr[0])):
        print('{0: <3}|'.format(i), end="")
    print()

    for i, line in enumerate(map_repr):
        print('{0: <3}|'.format(i), end="")
        for cell in line:
            print('{0: <3}|'.format(cell.strip()), end="")
        print()


class TestHumanReadable:

    @pytest.fixture(autouse=True)
    def map_representation(self):
        return [["T1", "O ", "O", "O", "T2", " "],
                ["  ", "  ", "O", "O", "O ", " "],
                ["A2", "  ", " ", "O", "  ", " "],
                ["  ", "  ", " ", " ", "  ", " "],
                ["  ", "A1", " ", " ", "  ", " "]]

    def test_extract_grid_representation(self, map_representation):
        (graph, entities) = humanreadable.extract_grid_information(map_representation)
        edges = graph.edges

        for entity in entities:
            print(entity)

        pretty_print_map(map_representation)

    def test_convert_to_grid_representation(self, map_representation):
        (graph, entities) = humanreadable.extract_grid_information(map_representation)
        new_representation = humanreadable._generate_grid_representation(graph.rows, graph.cols, entities)
        pretty_print_map(new_representation)

        for x in range(len(new_representation)):
            for y in range(len(new_representation[0])):
                assert new_representation[x][y].strip() == map_representation[x][y].strip()


