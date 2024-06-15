from enum import Enum, IntEnum
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


class MapScheme:
    """
        Represents a map for a benchmark execution. The name
        is used to avoid conflicts with the map() built-in Python function
    """
    def __init__(self, map_contents: np.array):
        """
            Object initialization

            Parameters
            ----------
            map_contents : list[list[MapContent]]
                List of the contents of the map

            Raises
            ------
            ValueError
                If the map is not a 2-dimensional array
        """
        map_contents = np.array(map_contents)
        if map_contents.ndim != 2:
            raise ValueError("Invalid map contents supplied: must be a 2-dimensional array")

        # Remove unrecognized content
        self._map_contents = np.clip(np.array(map_contents).copy(), MapContent.OBSTACLE, MapContent.FREE + 1)

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

    def has_position(self, position: tuple[int, int]) -> bool:
        """
            Checks if the supplied position is present in the map

            Parameters
            ----------
            position : tuple[int, int]
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
        return f"MapScheme(width={self._width}, height={self._height})"



