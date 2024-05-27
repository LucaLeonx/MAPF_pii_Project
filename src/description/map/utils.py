from nis import match

from description.benchmarkdescription import TestDescription
from description.entity_description import ObstacleDescription, AgentDescription, ObjectiveDescription
from description.map.graph import Graph, Edge, Node, GridGraph
from exceptions import InvalidElementException


def generate_grid_test(test_name, map_representation):
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

    return TestDescription(test_name, graph, agents + obstacles + objectives)


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
                case "":
                    break
                case "O":
                    break
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


def generate_grid_representation(rows, cols, entities):
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



