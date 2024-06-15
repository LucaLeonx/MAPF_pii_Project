'''
# May be useful in the future
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