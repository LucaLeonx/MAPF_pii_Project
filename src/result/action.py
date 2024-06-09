from description.map.graph import Node
from exceptions import ElementNotAvailableException

import importlib


class Action(object):

    def __init__(self, timestep: int, subject: str, start_position: Node = None, end_position: Node = None, description: str = ""):
        self._timestep = timestep
        self._subject = subject
        self._start_position = start_position
        self._end_position = end_position
        self._description = description

    def __str__(self) -> str:
        return "timestep: " + str(self.timestep) + " | Entity: " + self.subject + " | Position: " + str(self.start_position) + " | target:  " + str(self.end_position)  

    @property
    def timestep(self):
        return self._timestep

    @property
    def subject(self):
        return self._subject

    @property
    def start_position(self):
        # if self._start_position is None:
        #    raise ElementNotAvailableException("This action doesn't have a final position")

        return self._start_position

    @property
    def end_position(self):
        # if self._end_position is None:
        #    raise ElementNotAvailableException("This action doesn't have a final position")

        return self._end_position

    @property
    def description(self):
        return self._description

    @property
    def type(self):
        return self.__class__.__name__

    def to_dict(self):
        dictionary = {"type": self.type,
                      "timestep": self.timestep,
                      "subject": self.subject}

        if self._start_position is not None:
            dictionary.update({"start_position": self._start_position.to_dict()})
        if self._end_position is not None:
            dictionary.update({"end_position": self._end_position.to_dict()})

        dictionary.update({"description": self._description})
        return dictionary

    @staticmethod
    def from_dict(dictionary):
        module = importlib.import_module(__name__)
        action_class = getattr(module, dictionary["type"])
        start_position = None
        end_position = None

        if "start_position" in dictionary:
            start_position = Node.from_dict(dictionary.get("start_position"))
        if "end_position" in dictionary:
            end_position = Node.from_dict(dictionary.get("end_position"))

        return action_class(dictionary["timestep"],
                            dictionary["subject"],
                            start_position,
                            end_position,
                            dictionary["description"])


class MoveAction(Action):
    def __init__(self, timestep, subject, start_position, end_position, description=""):
        Action.__init__(self, timestep, subject, start_position, end_position, description)


class WaitAction(Action):
    def __init__(self, timestep, subject, start_position, end_position=None, description=""):
        Action.__init__(self, timestep, subject, start_position, end_position, description)


class AppearAction(Action):
    def __init__(self, timestep, subject, end_position, start_position=None,  description=""):
        Action.__init__(self, timestep, subject, None, end_position, description)


class DisappearAction(Action):
    def __init__(self, timestep, subject, start_position=None, end_position=None, description=""):
        Action.__init__(self, timestep, subject, None, None, description)
