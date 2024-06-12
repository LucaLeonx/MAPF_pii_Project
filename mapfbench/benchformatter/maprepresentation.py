from description.entity_description import ObstacleDescription, AgentDescription, ObjectiveDescription, \
    EntityDescription
from utilities.customexceptions import InvalidElementException

from description.graph import Node


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
                elif cell[0] == "O":
                    pass
                elif cell[0] == "A":
                    MapRepresentation._register_id(agents, cell, x, y, "agent")
                elif cell[0] == "T":
                    MapRepresentation._register_id(objectives, cell, x, y, "objective")
                else:
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
                map_representation[rows - 1 - position.y][position.x] = "A" + entity.name[1:].strip()
            elif entity.__class__.__name__ == "ObjectiveDescription":
                position = entity.start_position
                map_representation[rows - 1 - position.y][position.x] = "T" + entity.name[1:].strip()
            elif entity.__class__.__name__ == "ObstacleDescription":
                position = entity.start_position
                map_representation[rows - 1 - position.y][position.x] = "O"
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
                start_position = Node(coords=(y, rows - 1 - x))

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
