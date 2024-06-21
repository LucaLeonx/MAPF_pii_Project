import importlib
from abc import abstractmethod, ABC
from enum import IntEnum
from typing import Any

import numpy as np


class MapContent(IntEnum):
    """
        Enumeration representing the content of a single cell of a map.
        Each constant has an integer value associated.
        The logic behind is:
        - Free cells are associated to 0
        - Impediments (trees, water...) are associated to negative numbers
        - Agents have strictly positive IDs
    """
    FREE = 0
    OBSTACLE = -1

    # For later
    # SWAMP = -2
    # WATER = -3
    # OUT_OF_BOUND = -4

    @classmethod
    @property
    def values(self):
        return [e.value for e in MapContent]


class MapScheme(ABC):
    """
        Represents a map for a benchmark execution. The name
        is used to avoid conflicts with the map() built-in Python function
    """

    def __init__(self, map_contents: np.array):
        """
            Object initialization

            Parameters
            ----------
            map_contents : array_like
                List of the contents of the map. If any integer not present
                in MapContents.values is inserted, it is left as it is

            Raises
            ------
            ValueError
                If the map is not a 2-dimensional array
        """
        map_contents = np.array(map_contents)

        if map_contents.ndim > 3:
            raise ValueError("Invalid map contents supplied")

        self._map_contents = map_contents

        self._free_positions = np.transpose(np.nonzero(self._map_contents == MapContent.FREE))
        self._obstacle_positions = np.transpose(np.nonzero(self._map_contents == MapContent.OBSTACLE))

    @property
    @abstractmethod
    def dimensions(self) -> tuple[int, ...]:
        """
            The dimensions  of the map
        """
        pass

    @property
    def free_positions(self) -> np.array:
        """
            Returns the free positions of the map, in a 2-dimensional array.
            These position have content MapContent.FREE
        """
        return self._free_positions

    @property
    def obstacles(self) -> np.array:
        """
            Returns the free positions of the map, in a 2-dimensional array.
            These position have content MapContent.OBSTACLE
        """
        return self._obstacle_positions

    @property
    @abstractmethod
    def contents(self) -> np.array:
        """
            Returns the contents of the map. The format depends on the
            specific map instance used
        """
        return np.copy(self._map_contents)

    def has_position(self, position: tuple[int, ...]) -> bool:
        """
            Checks if the supplied position is present in the map

            Parameters
            ----------
            position : tuple[int
                The position to check for

            Returns
            -------
                True if the supplied position is present in the map, False otherwise
        """

        position = np.array(position)

        if position is None or np.array_equal(position, np.array(None)):
            return False
        elif position.ndim != 1 and position.size < 1:
            return False
        elif position[0] < 0 or position[0] >= self.height:
            return False
        elif position[1] < 0 or position[1] >= self.width:
            return False

        return True

    def __str__(self):
        return f"MapScheme"

    def encode(self) -> dict[str, Any]:
        return {"type": str(self.__class__.__name__), "contents": self._map_contents.tolist()}

    @staticmethod
    def decode(dictionary: dict[str, Any]) -> "MapScheme":
        map_types = importlib.import_module("mapfbench.description.maps.maptypes")
        map_class = getattr(map_types, dictionary["type"])
        return map_class(dictionary["contents"])
