import pytest
import numpy as np

from mapfbench.description import MapScheme, GridMap
from mapfbench.description.scenario import Scenario, Agent
from mapfbench.instrument.planrecorder import PlanRecorder


@pytest.fixture(autouse=True)
def generic_map_scheme():
    return GridMap(np.array([[0, -1, 0],
                               [0, -1, 0],
                               [0, 0, 0]]))


@pytest.fixture(autouse=True)
def generic_scenario(generic_map_scheme):
    return Scenario(generic_map_scheme,
                    [
                        Agent(1, (0, 1), (1, 0)),
                        Agent(2, (0, 2), (2, 0))])


@pytest.fixture(autouse=True)
def generic_plan(generic_scenario):
    recorder = PlanRecorder(generic_scenario)
    recorder.record_move(1, 1, (0, 2))
    recorder.record_move(1, 2, (1, 2))
    recorder.record_move(2, 1, (1, 2))
    recorder.record_wait(2, 2)

    recorder.mark_as_solved()

    return recorder.plan

