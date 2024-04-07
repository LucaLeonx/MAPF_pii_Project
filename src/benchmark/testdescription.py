from entity.agent_description import AgentDescription
from entity.objective_description import ObjectiveDescription
from entity.obstacle_description import ObstacleDescription


class TestDescription:
    
    def __init__(self, test_map, entities):
        self._map = test_map
        self._entities = entities
    
    def get_map(self):
        return self._map

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


