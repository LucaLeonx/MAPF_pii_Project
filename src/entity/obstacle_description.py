from entity.entity_description import EntityDescription
from graph.node import Node


class ObstacleDescription(EntityDescription):
    @staticmethod
    def from_dict(dictionary, use_coordinates=False):
        if "start_position" in dictionary:
            return ObstacleDescription(dictionary["name"], Node.from_dict(dictionary["start_position"], use_coordinates))
        else:
            return ObstacleDescription(dictionary["name"])

