from optional import Optional

from graph.node import Node


class EntityDescription:
    def __init__(self, name, start_position=None):
        if name != "":
            self._name = name
        else:
            raise ValueError("Entity Name cannot be empty")

        self._start_position = Optional.of(start_position)

    def get_name(self):
        return self._name

    def get_start_position(self):
        return self._start_position

    def has_start_position(self):
        return self._start_position.is_present()

    def __str__(self):
        return self.__class__.__name__ + " " + self._name + " " + (str(self._start_position.get()) if self.has_start_position() else "")

    def to_dict(self):
        new_dict = {"__class__": self.__class__.__name__,
                    "name": self._name}
        if self.has_start_position():
            new_dict.update({"start_position": self.get_start_position().get().to_dict()})

        return new_dict

    @staticmethod
    def from_dict(dictionary, use_coordinates=False):
        return EntityDescription(dictionary["name"])

