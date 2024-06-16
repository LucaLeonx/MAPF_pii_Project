import numpy as np
import pytest

from mapfbench.description import Plan, Action, ActionType
from mapfbench.metrics.metric import NumberOfConflicts
from mapfbench.metrics.result import PlanResults
from conftest import generic_scenario


# TODO make proper tests later


@pytest.fixture(autouse=True)
def plans(generic_scenario):
    return [
        (Plan(generic_scenario,
            np.array([
                Action(0, 1, ActionType.MOVE, [0, 1], [1, 1]),
                Action(0, 2, ActionType.WAIT, [0, 2], [0, 2]),
                Action(1, 1, ActionType.MOVE, [1, 1], [2, 1]),
                Action(1, 2, ActionType.MOVE, [0, 2], [1, 2])
            ], dtype=Action), True), 1),  # Conflicts number expected
        (Plan(generic_scenario,
              np.array([
                  Action(0, 1, ActionType.MOVE, [0, 1], [1, 2]), # Teleport
                  Action(0, 2, ActionType.WAIT, [0, 2], [0, 2]),
                  Action(1, 1, ActionType.MOVE, [1, 2], [0, 2]),
                  Action(1, 2, ActionType.MOVE, [0, 2], [1, 2])
              ], dtype=Action), True), 1), # No vertex conflict, at instant[0, 1] the agent moves
        (Plan(generic_scenario,
              np.array([
                  Action(0, 1, ActionType.MOVE, [0, 1], [1, 2]), # Teleport
                  Action(0, 2, ActionType.MOVE, [0, 2], [1, 2]),
              ], dtype=Action), True), 1),
        (Plan(generic_scenario,
              np.array([
                  Action(0, 1, ActionType.MOVE, [0, 1], [1, 2]),  # Teleport
                  Action(0, 2, ActionType.WAIT, [0, 2], [0, 2]),
              ], dtype=Action), True), 0),
    ]


class TestMetrics(object):
    def test_conflict(self, plans, generic_scenario):
        for plan, expected_conflict_num in plans:
            results = PlanResults(plan, [NumberOfConflicts()])
            #print([str(conflict) for conflict in results.results["Edge conflicts"]])
            assert results.results["Number of conflicts"] == expected_conflict_num
