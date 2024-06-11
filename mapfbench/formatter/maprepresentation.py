from description.entity_description import ObstacleDescription, AgentDescription, ObjectiveDescription, \
    EntityDescription

from utilities.customexceptions import InvalidElementException
from description.graph import Node

"""
def to_human_readable_dict(test: TestDescription):
    dictionary = test.to_dict()
    match test.graph.__class__.__name__:
        case "Graph":
            pass
        case "GridGraph":
            dictionary["graph"].update({"rows": test.graph.rows,
                                        "cols": test.graph.cols})
            try:
                map_conversion = MapRepresentation.from_entities(test.graph.rows, test.graph.cols, test.entities)
                dictionary["graph"].update({"map": map_conversion})
                dictionary.pop("entities")
            except InvalidElementException:
                dictionary["entities"] = test.to_dict().get["entities"]
                for entity_dict in dictionary["entities"].items():
                    position = entity_dict.get("start_position", None)

                    if position is not None:
                        node = Node(position["index"])
                        entity_dict.update({"start_position": {"x": node.x, "y": node.y}})

        case "UndirectedGraph":
            dictionary["graph"]["edges"] = [Edge.to_dict(edge)
                                            for edge in test.graph.undirected_edges]
        case _:
            raise InvalidElementException(f"Unsupported graph format for test: {test.name}")

    return dictionary


def from_human_readable_dict(dictionary: dict) -> TestDescription:
    test_name = dictionary["name"]
    entities = []

    match dictionary["graph"]["type"]:
        case "DirectedGraph":
            graph = Graph.from_dict(dictionary["graph"])
        case "UndirectedGraph":
            graph = UndirectedGraph(dictionary["graph"]["edges"])
        case "GridGraph":
            graph = GridGraph(dictionary["graph"]["rows"], dictionary["graph"]["cols"])
            entities += dictionary["graph"]["map"].entities
        case _:
            raise InvalidElementException(f"Error in graph representation in dictionary")

    if "entities" in dictionary:
        entities = [EntityDescription.from_dict(entity) for entity in dictionary["entities"]]

    return TestDescription(test_name, graph, entities)


def convert_to_human_readable_dict(benchmark: BenchmarkDescription) -> dict[str, Any]:
    dictionary = benchmark.to_dict()
    converted_tests = []
    for test in benchmark.tests:
        converted_tests.append(to_human_readable_dict(test))

    dictionary["tests"] = converted_tests

    return dictionary


def convert_from_human_readable_dict(dictionary: dict[str, Any]) -> BenchmarkDescription:
    test_occurrences = {}
    for test_dict in dictionary["tests"]:
        converted_test = from_human_readable_dict(test_dict)
        test_occurrences.update({converted_test: dictionary["test_occurrences"][converted_test.name]})

    return BenchmarkDescription(dictionary["name"], test_occurrences)

"""


class MapRepresentation:
    def __init__(self, representation: list[list[str]]):
        MapRepresentation.validate_map_representation(representation)
        self._representation = representation
        self._entities = self._extract_entities(representation)

    @property
    def representation(self) -> list[list[str]]:
        return self._representation

    @property
    def rows(self) -> int:
        return len(self._representation)

    @property
    def cols(self) -> int:
        return len(self._representation[0])

    @property
    def entities(self) -> list[EntityDescription]:
        return self._entities

    @staticmethod
    def validate_map_representation(representation):
        rows = len(representation)
        cols = len(representation[0])
        agents = set()
        objectives = set()

        for i in range(rows):
            if len(representation[i]) != cols:
                raise InvalidElementException("Mismatch between rows lengths")

        for x in range(rows):
            for y in range(cols):
                cell = representation[x][y].strip()

                if cell == "":
                    continue
                match cell[0]:
                    case "O":
                        pass
                    case "A":
                        MapRepresentation._register_id(agents, cell, x, y, "agent")
                    case "T":
                        MapRepresentation._register_id(objectives, cell, x, y, "objective")
                    case _:
                        raise InvalidElementException(f"Unrecognized cell content: {cell} at ({x}, {y})")

        if agents != objectives:
            if len(agents) > len(objectives):
                raise InvalidElementException(f"Missing objective for the agents with IDs: "
                                              f"{list(agents.difference(objectives))}")
            else:
                if len(agents) > len(objectives):
                    raise InvalidElementException(f"Missing agent for the objectives with IDs: "
                                                  f"{list(objectives.difference(agents))}")

    @staticmethod
    def _register_id(id_group: set[int], cell_content: str, x: int, y: int, label: str) -> None:
        try:
            entity_id = int(cell_content[1:])
            if entity_id < 0:
                raise InvalidElementException(f"Invalid negative ID: {entity_id} at ({x}, {y})")
            if entity_id in id_group:
                raise InvalidElementException(f"Duplicate {label} {id} inserted at ({x}, {y})")

            id_group.add(entity_id)
        except ValueError:
            raise InvalidElementException(f"Unrecognized cell content: {cell_content} at ({x}, {y})")

    @staticmethod
    def from_entities(rows: int, cols: int, entities: list[EntityDescription]):
        map_representation = [[" " for _ in range(cols)] for _ in range(rows)]

        for entity in entities:
            if not entity.has_start_position():
                raise InvalidElementException(f"Entity {entity} has no start position")
            if entity.__class__.__name__ == "AgentDescription":
                position = entity.start_position
                map_representation[position.x][position.y] = "A" + entity.name[1:].strip()
            elif entity.__class__.__name__ == "ObjectiveDescription":
                position = entity.start_position
                map_representation[position.x][position.y] = "T" + entity.name[1:].strip()
            elif entity.__class__.__name__ == "ObstacleDescription":
                position = entity.start_position
                map_representation[position.x][position.y] = "O"
            else:
                raise InvalidElementException(f"Invalid entity found")

        MapRepresentation.validate_map_representation(map_representation)
        return MapRepresentation(map_representation)

    def __str__(self):
        string = ""

        for line in self.representation:
            string += "|"
            for cell in line:
                string += cell.strip().center(5, " ") + "|"

            string += "|\n"

        return string

    def to_lines(self):
        return str(self).splitlines()

    @staticmethod
    def _extract_entities(representation) -> list[EntityDescription]:
        # representation = _to_cartesian_representation(representation)
        rows = len(representation)
        cols = len(representation[0])

        agents = []
        obstacles = []
        objectives = []

        for x in range(rows):
            for y in range(cols):
                cell = representation[x][y].strip()
                if len(cell) == 0:
                    continue

                # Reversal is necessary to make
                # the matrix position correspond to cartesian coordinates
                start_position = Node(coords=(x, y))

                if cell[0] == 'O':
                    obstacles.append(ObstacleDescription("O" + str(len(obstacles)), start_position))
                elif cell[0] == 'A':
                    agents.append(AgentDescription(cell, "T" + cell[1:], start_position))
                elif cell[0] == 'T':
                    objectives.append(ObjectiveDescription(cell, start_position))

        return agents + obstacles + objectives

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_scalar("!Map", str(data), style="|")

    @staticmethod
    def constructor(loader, node):
        map_str = loader.construct_scalar(node)
        lines = map_str.strip().split("||")

        map_representation = []

        # Remove empty list produced by splitting
        del lines[-1]

        for line in lines:
            # [1::] to remove newline at the beginning
            map_representation.append(line.split("|")[1::])

        return MapRepresentation(map_representation)


