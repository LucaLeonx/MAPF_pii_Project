from nis import match
from xml.dom.minidom import Entity

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

    for x in range(cols):
        for y in range(rows):

            cell = map_representation[x][y].strip()
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


def _generate_grid_representation(rows, cols, entities):
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


def to_human_readable_dict(test):
    dictionary = test.to_dict()
    match test.__class__.__name__:
        case "Graph":
            pass
        case "GridGraph":
            dictionary["graph"].update({"rows": test.graph.rows,
                                        "cols": test.graph.cols})
            try:

                dictionary["graph"].update({"map": _generate_grid_representation(test.graph.rows,
                                                                                 test.graph.cols,
                                                                                 test.entities)})
                dictionary["graph"].pop("edges")
                dictionary.pop("entities")
            except InvalidElementException:
                dictionary["entities"] = test.to_dict().get["entities"]
        case "UndirectedGraph":
            dictionary["graph"]["edges"] = [Edge.to_dict(edge)
                                            for edge in test.graph.undirected_edges]
        case _:
            raise InvalidElementException(f"Unsupported graph format for test: {test.name}")

    return dictionary


def from_human_readable_dict(dictionary):

    test_name = dictionary["name"]
    entities = []

    match dictionary["graph"]["type"]:
        case "directed":
            graph = Graph.from_dict(dictionary["graph"])
        case "undirected":
            graph = UndirectedGraph(dictionary["graph"]["edges"])
        case "grid":
            if dictionary["graph"]["map"]:
                graph, entities = _generate_grid_representation(dictionary["graph"]["map"])
            else:
                graph = GridGraph(dictionary["graph"]["rows"], dictionary["graph"]["cols"])
        case _:
            raise InvalidElementException(f"Error in graph representation in dictionary")

    if dictionary["graph"]["type"] != "grid" and not dictionary["graph"]["map"]:
        entities = [EntityDescription.from_dict(entity) for entity in dictionary["entities"]]

    return TestDescription(test_name, graph, entities)
