import pytest

from mapfbench.metrics import PlanResults, Makespan, SumOfCosts, NumberOfAgents, MapDimensions


class TestPlanResult:

    def test_plan_result(self, generic_plan):
        plan_result = PlanResults(generic_plan)
        plan_result.evaluate([NumberOfAgents(), MapDimensions(), Makespan(), SumOfCosts()])
        assert plan_result.data.scenario.map.width == 3
        print(plan_result.results)
        assert plan_result.results == {'Number of agents': 2,
                                       'Map dimensions': (3, 3),
                                       'Makespan': 2,
                                       'Sum of costs': 4}
