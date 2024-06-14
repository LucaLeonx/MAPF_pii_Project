import numpy as np
from mapfbench.description.mapscheme import MapScheme


def sketch():
    # Check dimensions of empty obstacles array
    map = MapScheme(np.array([[0, 0, 0], [0, 0, 0]]))
    print(map.obstacles)
    print(map.obstacles.shape)


if __name__ == "__main__":
    sketch()
