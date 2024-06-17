import numpy as np
import pytest

from mapfbench.description import Plan, Action, ActionType
from mapfbench.metrics.metrics import Makespan, NumberOfAgents, AverageMakespan

from conftest import generic_scenario
from mapfbench.metrics.new_results import PlanResults, AggregatePlanResults


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
              ], dtype=Action)), 1),  # Conflicts number expected
        (Plan(generic_scenario,
              np.array([
                  Action(0, 1, ActionType.MOVE, [0, 1], [1, 2]),  # Teleport
                  Action(0, 2, ActionType.WAIT, [0, 2], [0, 2]),
                  Action(1, 1, ActionType.MOVE, [1, 2], [0, 2]),
                  Action(1, 2, ActionType.MOVE, [0, 2], [1, 2])
              ], dtype=Action)), 1),  # No vertex conflict, at instant[0, 1] the agent moves
        (Plan(generic_scenario,
              np.array([
                  Action(0, 1, ActionType.MOVE, [0, 1], [1, 2]),  # Teleport
                  Action(0, 2, ActionType.MOVE, [0, 2], [1, 2]),
              ], dtype=Action)), 1),
        (Plan(generic_scenario,
              np.array([
                  Action(0, 1, ActionType.MOVE, [0, 1], [1, 2]),  # Teleport
                  Action(0, 2, ActionType.WAIT, [0, 2], [0, 2]),
              ], dtype=Action)), 0),
    ]


class TestMetrics(object):
    def test_conflict(self, plans, generic_scenario):

        results = AggregatePlanResults([plan[0] for plan in plans], [])
        recursive_dict_print(results.results_dict)
        results.evaluate()
        #print(results.results)

        for plan, expected_conflict_num in plans:
            results = PlanResults(plan)
            results.evaluate()
            #print(results.results)


def recursive_dict_print(dictionary):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            print(f'{key}: ')
            recursive_dict_print(value)
        else:
            print(f'{key}: {value}')