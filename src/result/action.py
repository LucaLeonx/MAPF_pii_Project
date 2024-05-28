from description.map.graph import Node
from exceptions import ElementNotAvailableException

import importlib


class Action(object):

    def __init__(self, timestep, subject, position=None, description=""):
        self._timestep = timestep
        self._subject = subject
        self._position = position
        self._description = description

    @property
    def timestep(self):
        return self._timestep

    @property
    def subject(self):
        return self._subject

    @property
    def position(self):
        if self._position is None:
            raise ElementNotAvailableException("This action doesn't have a final position")

        return self._position

    @property
    def description(self):
        return self._description

    def to_dict(self):
        dictionary = {"type": self.__class__.__name__,
                      "timestep": self.timestep,
                      "subject": self.subject}

        if self._position is not None:
            dictionary.update({"position": self._position.to_dict()})

        dictionary.update({"description": self._description})
        return dictionary

    @staticmethod
    def from_dict(dictionary):
        module = importlib.import_module(__name__)
        action_class = getattr(module, dictionary["type"])

        if "position" in dictionary:
            position = Node.from_dict(dictionary.get("position"))
        else:
            position = None

        return action_class(dictionary["timestep"],
                            dictionary["subject"],
                            position,
                            dictionary["description"])


class MoveAction(Action):
    def __init__(self, timestep, subject, position, description="Move"):
        Action.__init__(self, timestep, subject, position, description)


class WaitAction(Action):
    def __init__(self, timestep, subject, position=None, description="Wait"):
        Action.__init__(self, timestep, subject, position, description)


class AppearAction(Action):
    def __init__(self, timestep, subject, position, description="Appear"):
        Action.__init__(self, timestep, subject, position, description)


class DisappearAction(Action):
    def __init__(self, timestep, subject, description="Disappear"):
        Action.__init__(self, timestep, subject, None, description)
