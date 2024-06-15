import pytest
import numpy as np

from mapfbench.description.mapscheme import MapScheme
from mapfbench.description.scenario import Scenario, Agent


@pytest.fixture(autouse=True)
def generic_map_scheme():
    return MapScheme(np.array([[0, -1, 0],
                               [0, -1, 0],
                               [0, 0, 0]]))


@pytest.fixture(autouse=True)
def generic_scenario(generic_map_scheme):
    return Scenario(generic_map_scheme,
                    [Agent(1, (0, 1), (1, 0)),
                     Agent(2, (0, 2), (2, 0))])
