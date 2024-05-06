from entity.agent_description import AgentDescription
from entity.entity_description import EntityDescription
from entity.objective_description import ObjectiveDescription
from entity.obstacle_description import ObstacleDescription
from graph.graph import Graph


class TestDescription:

    def __init__(self, name, test_map, entities):
        if name != "":
            self._name = name
        else:
            raise ValueError("Name cannot be empty")

        self._test_map = test_map
        self._entities = entities

    def get_name(self):
        return self._name

    def get_test_map(self):
        return self._test_map

    def get_entities(self):
        return self._entities

    def _get_entities_by_class(self, selected_class):
        return [entity for entity in self._entities if isinstance(entity, selected_class)]

    def get_agents(self):
        return self._get_entities_by_class(AgentDescription)

    def get_obstacles(self):
        return self._get_entities_by_class(ObstacleDescription)

    def get_objectives(self):
        return self._get_entities_by_class(ObjectiveDescription)

    def __str__(self):
        string = self._name + ":\n" + "Map: \n" + str(self._test_map) + "\n"
        for entity in self._entities:
            string += str(entity) + "\n"
        return string

    def to_dict(self):
        return {"name": self._name,
                "test_map": self._test_map.to_dict(),
                "entities": [entity.to_dict() for entity in self._entities]}

    @staticmethod
    def from_dict(dictionary, use_coordinates=False):

        entities = []
        for entity in dictionary["entities"]:
            match entity["__class__"]:
                case "AgentDescription":
                    entities.append(AgentDescription.from_dict(entity, use_coordinates))
                case "ObjectiveDescription":
                    entities.append(ObjectiveDescription.from_dict(entity, use_coordinates))
                case "ObstacleDescription":
                    entities.append(ObstacleDescription.from_dict(entity, use_coordinates))
                case _:
                    raise ValueError("Unknown entity type encountered")

        return TestDescription(dictionary["name"],
                               Graph.from_dict(dictionary["test_map"], use_coordinates),
                               entities)
