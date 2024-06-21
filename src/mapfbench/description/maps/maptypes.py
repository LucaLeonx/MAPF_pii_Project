from typing import Any

import numpy as np

from mapfbench.description.maps.mapscheme import MapScheme, MapContent


class GridMap(MapScheme):
    """
        Represents a map for a benchmark execution. The name
        is used to avoid conflicts with the map() built-in Python function
    """

    def __init__(self, map_contents: np.array):
        """
            Object initialization

            Parameters
            ----------
            map_contents : array_like[2, 2]
                List of the contents of the map. If any integer not present
                in MapContents.values is inserted, it is left as it is

            Raises
            ------
            ValueError
                If the map is not a 2-dimensional array
        """
        super().__init__(map_contents)
        if map_contents.ndim != 2:
            raise ValueError("Invalid map contents supplied: must be a 2-dimensional array")

        self._map_contents = map_contents
        self._width = map_contents.shape[1]
        self._height = map_contents.shape[0]

        self._free_positions = np.transpose(np.nonzero(self._map_contents == MapContent.FREE))
        self._obstacle_positions = np.transpose(np.nonzero(self._map_contents == MapContent.OBSTACLE))

    @property
    def width(self) -> int:
        """
            The width of the map, in cells
        """
        return self._width

    @property
    def height(self) -> int:
        """
            The height of the map, in cells
        """
        return self._height

    @property
    def dimensions(self) -> tuple[int, ...]:
        """
            The dimensions (width, height) of the map
        """
        return self._width, self._height

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
    def contents(self) -> np.array:
        """
            Returns the contents of the map, as a matrix
        """
        return np.copy(self._map_contents)

    def has_position(self, position: tuple[int, ...]) -> bool:
        """
            Checks if the supplied position is present in the map

            Parameters
            ----------
            position : tuple[int, ...]
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
        elif position.size != 2:
            return False
        elif position[0] < 0 or position[0] >= self.height:
            return False
        elif position[1] < 0 or position[1] >= self.width:
            return False

        return True

    def __str__(self):
        return f"GridMap(width={self._width}, height={self._height})"

    def encode(self) -> dict[str, Any]:
        return {"type": "GridMap", "contents": self._map_contents.tolist()}

    @staticmethod
    def decode(dictionary: dict[str, Any]) -> "GridMap":
        return GridMap(dictionary["contents"])


class VoxelGridMap(MapScheme):
    def __init__(self, map_contents: np.ndarray) -> None:
        super().__init__(map_contents)
        if map_contents.ndim != 2:
            raise ValueError("Invalid map contents supplied: must be a 3-dimensional array")

        self._width = map_contents.shape[1]
        self._height = map_contents.shape[0]
        self._depth = map_contents.shape[2]

        self._free_positions = np.transpose(np.nonzero(self._map_contents == MapContent.FREE))
        self._obstacle_positions = np.transpose(np.nonzero(self._map_contents == MapContent.OBSTACLE))

    @property
    def width(self) -> int:
        """
            The width of the map, in cells
        """
        return self._width

    @property
    def height(self) -> int:
        """
            The height of the map, in cells
        """
        return self._height

    @property
    def depth(self):
        """
            The depth of the map, in cells
        """
        return self._depth

    @property
    def dimensions(self) -> tuple[int, ...]:
        """
            The dimensions (width, height, depth) of the map
        """
        return self._width, self._height, self._depth

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
    def contents(self) -> np.array:
        """
            Returns the contents of the map, as a matrix
        """
        return np.copy(self._map_contents)

    def has_position(self, position: tuple[int, ...]) -> bool:
        """
            Checks if the supplied position is present in the map

            Parameters
            ----------
            position : tuple[int, ...]
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
        elif position.size != 3:
            return False
        elif position[0] < 0 or position[0] >= self.height:
            return False
        elif position[1] < 0 or position[1] >= self.width:
            return False
        elif position[2] < 0 or position[2] >= self.depth:
            return False

        return True

    def __str__(self):
        return f"VoxelGridMap(width={self._width}, height={self._height}, depht={self._depth})"

    def encode(self) -> dict[str, Any]:
        return {"type": "VoxelGridMap", "contents": self._map_contents.tolist()}

    @staticmethod
    def decode(dictionary: dict[str, Any]) -> "VoxelGridMap":
        return VoxelGridMap(dictionary["contents"])


class GraphMap(MapScheme):
    def __init__(self, contents: list[tuple[int, int, int]], undirected: bool = False):
        if undirected:
            actual_contents = contents + [(edge[1], edge[0], edge[2]) for edge in contents]
        else:
            actual_contents = contents
        map_contents = np.array(actual_contents, dtype=[('start', '<U10'), ('end', '<U10'), ('weight', '<f4')])
        super().__init__(map_contents)
        self._undirected = undirected

        self._nodes = np.concatenate((self._map_contents["start"], self._map_contents["end"]))

    @property
    def nodes(self) -> np.ndarray:
        return self._nodes

    @property
    def edges(self) -> np.ndarray:
        return self._map_contents

    @property
    def undirected(self) -> bool:
        return self._undirected
