"Module representing a map, with its content"
from enum import Enum, IntEnum
import numpy as np

'''
class Cell:
    """
        Represents a single cell in a MapScheme
    """
    def __init__(self, x : int, y : int):
        """
            Object initialization
        Parameters
        ----------
        x : int
            x coordinate of the cell
        y : int
            y coordinate of the cell

        """
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        """
        Return
        ------
            The x coordinate of the cell
        """
        return self._x

    @property
    def y(self) -> int:
        """
        Return
        ------
            The y coordinate of the cell
        """
        return self._y

    @property
    def coords(self) -> tuple[int, int]:
        """
        Return
        ------
            The coordinates of the cell
        """
        return self._x, self._y
'''


class MapContent(IntEnum):
    FREE = 0
    OBSTACLE = -1
    # WATER = -2
    # SWAMP = -3


class MapScheme:
    """
        Represents a map for a benchmark execution. The name
        is used to avoid conflicts with the map() built-in Python function
    """

    def __init__(self, map_contents: np.array):
        if map_contents.ndim != 2:
            raise ValueError("Invalid map contents supplied: must be a 2-dimensional array")

        # Remove unrecognized content
        self._map_contents = np.clip(map_contents.copy(), MapContent.OBSTACLE, MapContent.FREE + 1)

        self._width = map_contents.shape[1]
        self._height = map_contents.shape[0]

        self._free_positions = np.transpose(np.nonzero(self._map_contents == MapContent.FREE))
        self._obstacle_positions = np.transpose(np.nonzero(self._map_contents == MapContent.OBSTACLE))

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def free_positions(self) -> np.array:
        return self._free_positions

    @property
    def obstacles(self) -> np.array:
        return self._obstacle_positions


class Agent:
    def __init__(self, agent_id: int, start_position: tuple[int, int], objective_position: tuple[int, int]):
        self._id = agent_id
        self._start_position = start_position
        self._objective_position = objective_position

    @property
    def id(self) -> int:
        return self._id

    @property
    def start_position(self) -> tuple[int, int]:
        return self._start_position

    @property
    def objective_position(self) -> tuple[int, int]:
        return self._objective_position

