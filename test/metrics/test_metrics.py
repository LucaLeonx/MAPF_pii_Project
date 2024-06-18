import numpy as np
import pytest

from mapfbench.description import Plan, Action, ActionType
from mapfbench.exporter import exporter
from mapfbench.metrics.metrics import Makespan, NumberOfAgents, AverageMakespan, AgentId, SuccessRate

from mapfbench.metrics.results import PlanResults, AggregatePlanResults, AgentResults


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

        results = AggregatePlanResults([plan[0] for plan in plans])
        results.evaluate([SuccessRate()])
        print(results.inner_results[0].results_dict)
        exporter.export_plans(results, "prova")


        plan = plans[0][0]

        #results = AgentResults(list(plan.agent_plans.items())[0])
        #results.evaluate()
        #print(results.results)
        #results = PlanResults(plan)
        #results.evaluate()
        #print(results.results)
