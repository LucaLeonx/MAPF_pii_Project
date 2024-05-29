import yaml

from description.benchmarkdescription import TestDescription
from description.entity_description import ObstacleDescription, AgentDescription, ObjectiveDescription, \
    EntityDescription
from description.map.graph import Graph, Edge, Node, GridGraph, UndirectedGraph
from exceptions import InvalidElementException


def extract_grid_information(map_representation):
    rows = len(map_representation)
    cols = len(map_representation[0])
    graph = GridGraph(rows, cols)

    agents = []
    obstacles = []
    objectives = []

    for x in range(rows):
        for y in range(cols):
            cell = map_representation[x][y].strip()
            if len(cell) == 0:
                continue

            match cell[0]:
                case 'O':
                    obstacles.append(ObstacleDescription("O" + str(len(obstacles)), Node(coords=(x, y))))
                case 'A':
                    agents.append(AgentDescription(cell, "T" + cell[1:], Node(coords=(x, y))))
                case 'T':
                    objectives.append(ObjectiveDescription(cell, Node(coords=(x, y))))

    return graph, agents + obstacles + objectives


def validate_map_representation(map_representation):
    rows = len(map_representation)
    cols = len(map_representation[0])
    agents = set()
    objectives = set()

    for i in range(rows):
        if len(map_representation[i]) != cols:
            raise InvalidElementException("Mismatch between rows lengths")

    for x in range(cols):
        for y in range(rows):
            cell = map_representation[x][y].strip()
            match cell[0]:
                case "" | "O":
                    pass
                case "A":
                    _register_id(agents, cell, x, y, "agent")
                case "T":
                    _register_id(objectives, cell, x, y, "objective")
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


def _register_id(id_group, cell, x, y, label):
    try:
        entity_id = int(cell[1:])
        if entity_id < 0:
            raise InvalidElementException(f"Invalid negative ID: {entity_id} at ({x}, {y})")
        if entity_id in id_group:
            raise InvalidElementException(f"Duplicate {label} {id} inserted at ({x}, {y})")

        id_group.add(entity_id)
    except ValueError:
        raise InvalidElementException(f"Unrecognized cell content: {cell} at ({x}, {y})")


def _generate_grid_representation(rows: int, cols: int, entities: list[EntityDescription]) -> list[list[str]]:
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

    return map_representation


def to_human_readable_dict(test: TestDescription):
    dictionary = test.to_dict()
    match test.graph.__class__.__name__:
        case "Graph":
            pass
        case "GridGraph":
            dictionary["graph"].update({"rows": test.graph.rows,
                                        "cols": test.graph.cols})
            try:
                grid = MapRepresentation(_generate_grid_representation(test.graph.rows, test.graph.cols, test.entities))
                dictionary["graph"].update({"map": grid})
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


def from_human_readable_dict(dictionary) -> TestDescription:
    test_name = dictionary["name"]
    entities = []

    match dictionary["graph"]["type"]:
        case "DirectedGraph":
            graph = Graph.from_dict(dictionary["graph"])
        case "UndirectedGraph":
            graph = UndirectedGraph(dictionary["graph"]["edges"])
        case "GridGraph":
            if dictionary["graph"]["map"]:
                graph, entities = extract_grid_information(dictionary["graph"]["map"].representation)
            else:
                graph = GridGraph(dictionary["graph"]["rows"], dictionary["graph"]["cols"])
        case _:
            raise InvalidElementException(f"Error in graph representation in dictionary")

    if dictionary["graph"]["type"] != "grid" and "map" not in dictionary["graph"]:
        entities = [EntityDescription.from_dict(entity) for entity in dictionary["entities"]]

    return TestDescription(test_name, graph, entities)


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
    def representer(dumper, data):
        serialized = ""
        representation = data.representation

        for line in representation:
            serialized += "|"
            for cell in line:
                serialized += cell.strip().center(5, " ") + "|"

            serialized += "|\n"

        return dumper.represent_scalar("!Map", serialized, style="|")

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
