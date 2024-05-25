from math import floor, sqrt


class Node:

    @classmethod
    def _cantor_pairing_function(cls, numbers):
        a, b = numbers
        return (a + b) * (a + b + 1) // 2 + b

    @classmethod
    def _cantor_inverse_pairing_function(cls, n):
        w = floor((sqrt(8 * n + 1) - 1) / 2)
        t = (w ** 2 + w) / 2
        return int(w - n + t), int(n - t)

    def __init__(self, index=None, coordinates=None):
        if index is None and coordinates is None:
            raise ValueError("A Node must be identified by either its index or its coordinates")
        elif index is not None:
            if index < 0:
                raise ValueError("The node index cannot be negative")
            else:
                self._index = index
                self._x, self._y = self._cantor_inverse_pairing_function(index)
        else:
            if coordinates[0] < 0 or coordinates[1] < 0:
                raise ValueError("The node coordinates cannot be negative")
            else:
                self._index = self._cantor_pairing_function(coordinates)
                self._x, self._y = coordinates

    def get_index(self):
        return self._index

    def get_coordinates(self):
        return self._x, self._y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self._index == other.get_index())

    def __hash__(self):
        return hash(self._index)

    def __str__(self):
        return f"{self._index} [{self._x}, {self._y}]"

    def to_dict(self, use_coordinates=False):
        if not use_coordinates:
            return {"index": self._index}
        else:
            return {"x": self._x, "y": self._y}

    @staticmethod
    def from_dict(dictionary, use_coordinates=False):
        if not use_coordinates:
            return Node(index=dictionary["index"])
        else:
            return Node(coordinates=(dictionary["x"], dictionary["y"]))
