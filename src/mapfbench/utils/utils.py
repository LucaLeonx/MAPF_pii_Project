import numpy as np


def position_not_null(position: np.array) -> bool:
    return position is not None and not np.array_equal(position, np.array(None))
