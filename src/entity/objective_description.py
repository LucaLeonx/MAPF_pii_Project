from entity.entity_description import EntityDescription
from graph.node import Node


class ObjectiveDescription(EntityDescription):
    @staticmethod
    def from_dict(dictionary, use_coordinates=False):
        if "start_position" in dictionary:
            return ObjectiveDescription(dictionary["name"], Node.from_dict(dictionary["start_position"], use_coordinates))
        else:
            return ObjectiveDescription(dictionary["name"])
