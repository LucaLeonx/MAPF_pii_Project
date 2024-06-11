import importlib
from abc import ABC
from typing import Optional

from customexceptions import EmptyElementException
from description.graph import Node


class EntityDescription(ABC):
    """
        Abstract class representing an entity of the test
    """
    def __init__(self, name: str, start_position: Optional[Node] = None):
        """
            Object initializer

            Parameters
            ----------
            name: str
                The identifying name of the entity
            start_position: Node, optional
                The initial position of the entity

            Raises
            ------
            EmptyElementException
                If the name is an empty string
        """
        if name.strip() == "":
            raise EmptyElementException("Entity name cannot be empty")

        self._name = name
        self._start_position = start_position

    @property
    def name(self) -> str:
        """
            The name of the entity
        """
        return self._name

    @property
    def start_position(self) -> Optional[Node]:
        """
            The start_position of the entity, if defined
        """
        return self._start_position

    def has_start_position(self) -> bool:
        return self._start_position is not None

    def __eq__(self, other):
        if isinstance(other, EntityDescription):
            return self.name == other.name

        return False

    def __str__(self):
        return (self.__class__.__name__ + " " + self._name + " " +
                (str(self._start_position) if self.has_start_position() else ""))

    def to_dict(self):
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
    """
        An agent in the test
    """
    def __init__(self, name: str, objective_name: str, start_position: Optional[Node] =None):
        """
            Object initializer

            Parameters
            ----------
            name: str
                The identifying name of the agent
            objective_name: str
                The name of the objective of the agent
            start_position: Node, optional
                The initial position of the agent

            Raises
            ------
            EmptyElementException
                If the name of the agent or the objective name are an empty string
        """
        if objective_name.strip() == "":
            raise EmptyElementException("Agent's objective name cannot be empty")

        EntityDescription.__init__(self, name, start_position)
        self._objective_name = objective_name

    @property
    def objective_name(self):
        """
            The name of the objective of the agent
        """
        return self._objective_name

    def to_dict(self):
        new_dict = super(AgentDescription, self).to_dict()
        new_dict.update({"objective": self.objective_name})
        return new_dict

    def __str__(self):
        return super(AgentDescription, self).__str__() + ", objective: " + self.objective_name


class ObjectiveDescription(EntityDescription):
    """
        An objective in the test
    """
    pass


class ObstacleDescription(EntityDescription):
    """
        An obstacle in the test
    """
    pass
