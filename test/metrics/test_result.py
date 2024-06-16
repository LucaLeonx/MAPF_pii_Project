import pytest

from mapfbench.metrics.metric import Makespan, SumOfCosts
from mapfbench.metrics.result import PlanResults


class TestPlanResult:

    def test_plan_result(self, generic_plan):
        plan_result = PlanResults(generic_plan, metrics=[Makespan(), SumOfCosts()])
        assert plan_result.plan.scenario.map.width == 3
        print(plan_result.results)
        assert plan_result.results == {'Number of agents': 2,
                                       'Map dimensions': (3, 3),
                                       'Obstacle density': 0.2222222222222222,
                                       'Makespan': 2,
                                       'Agents':
                                           {'Agent_1':
                                                {'Time Taken': 2},
                                            'Agent_2':
                                                {'Time Taken': 2}
                                            },
                                       'Sum of costs': 4}
