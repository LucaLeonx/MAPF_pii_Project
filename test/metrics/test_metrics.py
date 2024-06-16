import pytest

from mapfbench.description import plan

# TODO make proper tests later

"""
class TestMetrics(object):
    def test_results(self):

        result = Result.evaluate(MakeSpan, SumOfCosts, AverageCost, FuelCost(label = "Fuel in Euclidean", distance_metric=euclidean))
        aggregate_result = Result.evaluate(AverageMakeSpan, AverageSumOfCosts)

        # A unique dictionary of results, passed recursively. Parallel requests are queued to an executor,
        # which removes duplicate requests

        assert result.data == {"_makespan": 1, "_sum_of_costs": 2, "_average_cost": 0.4, "_fuel_cost": 0.2}
        assert result.payload.scenario.map.width == plan.scenario.map.width
        assert result.to_dict(use_labels=True, results_depth=2) == {
            "Makespan" : 0,
            "Sum Of Costs" : 1,
            "Fuel in Euclidean" : 2,
            "_test_1":
                "_makespan":
                "_sum_of_costs":
                "_average_cost":
                "_agents":
                    "_agent_0":


        }
        assert result1.
        assert result.full_dict()
"""