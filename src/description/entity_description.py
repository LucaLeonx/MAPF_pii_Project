import importlib
from abc import ABC

from description.map.graph import Node
from exceptions import EmptyElementException


class EntityDescription(ABC):
    def __init__(self, name, start_position=None):
        if name.strip() == "":
            raise EmptyElementException("Entity name cannot be empty")

        self._name = name
        self._start_position = start_position

    @property
    def name(self):
        return self._name

    @property
    def start_position(self):
        return self._start_position

    def has_start_position(self):
        return self._start_position is not None

    def __str__(self):
        return (self.__class__.__name__ + " " + self._name + " " +
                (str(self._start_position) if self.has_start_position() else ""))

    def to_dict(self, use_coords=False):
        new_dict = {"type": self.__class__.__name__,
                    "name": self._name}
        if self.has_start_position():
            new_dict.update({"start_position": self.start_position.to_dict()})

        return new_dict

    @staticmethod
    def from_dict(dictionary):
        module = importlib.import_module(__name__)
        entity_class = getattr(module, dictionary["type"])

        if "start_position" in dictionary:
            start_position = Node.from_dict(dictionary.get("start_position"))
        else:
            start_position = None

        if "objective" in dictionary:
            return AgentDescription(dictionary["name"], dictionary["objective"], start_position)
        else:
            return entity_class(dictionary["name"], start_position)


class AgentDescription(EntityDescription):
    def __init__(self, name, objective_name, start_position=None):
        if objective_name == "":
            raise ValueError("Agent's objective name cannot be empty")

        EntityDescription.__init__(self, name, start_position)
        self._objective_name = objective_name

    @property
    def objective_name(self):
        return self._objective_name

    def to_dict(self, use_coords=False):
        new_dict = super(AgentDescription, self).to_dict()
        new_dict.update({"objective": self.objective_name})
        return new_dict

    def __str__(self):
        return super(AgentDescription, self).__str__() + ", objective: " + self.objective_name


class ObjectiveDescription(EntityDescription):
    pass


class ObstacleDescription(EntityDescription):
    pass
