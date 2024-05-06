from entity.entity_description import EntityDescription
from graph.node import Node


class AgentDescription(EntityDescription):
    def __init__(self, name, objective_name, start_position=None):
        if objective_name == "":
            raise ValueError("Agent's objective name cannot be empty")

        EntityDescription.__init__(self, name, start_position)
        self._objective_name = objective_name

    def get_objective_name(self):
        return self._objective_name

    def to_dict(self):
        new_dict = super(AgentDescription, self).to_dict()
        new_dict.update({"objective_name": self.get_objective_name()})
        return new_dict

    def __str__(self):
        return super(AgentDescription, self).__str__() + ", objective: " + self.get_objective_name()

    @staticmethod
    def from_dict(dictionary, use_coordinates=False):
        if "start_position" in dictionary:
            return AgentDescription(dictionary["name"],
                                    dictionary["objective_name"],
                                    Node.from_dict(dictionary["start_position"], use_coordinates))
        else:
            return AgentDescription(dictionary["name"], dictionary["objective_name"])

