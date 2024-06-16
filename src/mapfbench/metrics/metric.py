from abc import ABC, abstractmethod
from typing import Any, Union

import numpy as np

from mapfbench.description import Plan, Agent, Action


class Metric(ABC):

    def __init__(self, identifier: str):
        self._identifier = identifier

    @property
    def identifier(self):
        return self._identifier

    @abstractmethod
    def evaluate(self, data, partial_results: dict[str, Any]) -> Any:
        if self.identifier not in partial_results:
            partial_results.update({self.identifier: None})
        if partial_results[self.identifier] is not None and partial_results[self.identifier] != {}:
            return partial_results[self.identifier]


# TODO add manhattan distance and other custom distances
def euclidean_distance(a: np.array, b: np.array):
    return np.linalg.norm(a - b)


# Just an alias to the function, for convenience
euclidean = euclidean_distance


class AggregateAgentMetric(Metric):
    @abstractmethod
    def evaluate(self, data: Plan, partial_results: dict[str, Any]) -> Any:
        super().evaluate(data, partial_results)
        if "_agents" not in partial_results:
            partial_results.update({"_agents": {}})

        for agent_id in data.scenario.agent_ids:
            if "_agent_" + str(agent_id) not in partial_results["_agents"]:
                partial_results["_agents"].update({"_agent_" + str(agent_id): {}})


class AggregatePlanMetric(Metric):
    @abstractmethod
    def evaluate(self, data: list[Plan], partial_results: dict[str, Any]) -> Any:
        super().evaluate(data, partial_results)
        if "_plans" not in partial_results:
            partial_results.update({"_plans": {}})
        for index, plan in enumerate(data):
            partial_results["_plans"].update({"_plan_" + str(index + 1): {}})


class Distance(Metric):
    def __init__(self):
        super().__init__("_distance")

    def evaluate(self, data: list[Action], partial_results: dict[str, Any]) -> float:
        super().evaluate(data, partial_results)
        result = sum([euclidean_distance(action.end_position, action.start_position) for action in data])
        partial_results.update({self.identifier: result})


class MaxTime(Metric):
    def __init__(self):
        super().__init__("_max_time")

    def evaluate(self, data: list[Action], partial_results: dict[str, Any]) -> int:
        super().evaluate(data, partial_results)

        if len(data) == 0:
            return 0

        result = max([action.timestep for action in data])
        partial_results.update({self.identifier: result})
        return result


class SumOfCosts(AggregateAgentMetric):
    def __init__(self):
        super().__init__("_sum_of_costs")

    def evaluate(self, data: Plan, partial_results: dict[str, Any]) -> int:
        super().evaluate(data, partial_results)
        result = 0
        for agent, plan in data.agent_plans.items():
            result += MaxTime().evaluate(plan, partial_results["_agents"]["_agent_" + str(agent.id)])

        partial_results.update({self.identifier: result})
        return result


class Makespan(AggregateAgentMetric):
    def __init__(self):
        super().__init__("_makespan")

    def evaluate(self, data: Plan, partial_results: dict[str, Any]) -> int:
        super().evaluate(data, partial_results)
        result = 0
        for agent, plan in data.agent_plans.items():
            result = max(result, MaxTime().evaluate(plan, partial_results["_agents"]["_agent_" + str(agent.id)]))

        partial_results.update({self.identifier: result})
        return result


class AverageMakespan(AggregateAgentMetric):
    def __init__(self):
        super().__init__("_avg_makespan")

    def evaluate(self, data: list[Plan], partial_results: dict[str, Any]):
        plans_num = len(data)
        result = 0

        if plans_num != 0:
            makespan_sum = 0
            for index, plan in enumerate(data, 1):
                makespan_sum += SumOfCosts().evaluate(plan, partial_results["_plans"]["_plan_" + str(index)])

            return makespan_sum / plans_num

        partial_results.update({self.identifier: result})
        return result


class NumberOfPlans(AggregatePlanMetric):
    def __init__(self):
        super().__init__("_num_of_plans")

    def evaluate(self, data: list[Plan], partial_results: dict[str, Any]) -> int:
        super().evaluate(data, partial_results)
        result = len(data)
        partial_results.update({self.identifier: result})
        return result


class MultipleMetric(Metric):
    def __init__(self, identifier: str, metrics: list[Metric]):
        super().__init__(identifier)
        self._metrics = metrics

    @property
    def metrics(self) -> list[Metric]:
        return self._metrics

    def evaluate(self, data: Union[Plan, list[Plan]], partial_results: dict[str, Any]) -> None:
        for metric in self._metrics:
            metric.evaluate(data, partial_results)


class NumberOfAgents(Metric):
    def __init__(self):
        super().__init__("_num_of_agents")

    def evaluate(self, data: Plan, partial_results: dict[str, Any]) -> int:
        super().evaluate(data, partial_results)
        result = data.scenario.agents_num
        partial_results.update({self.identifier: result})
        return result


class MapDimensions(Metric):
    def __init__(self):
        super().__init__("_map_dimensions")

    def evaluate(self, data: Plan, partial_results: dict[str, Any]) -> tuple[int, int]:
        super().evaluate(data, partial_results)
        plan_map = data.scenario.map
        result = (plan_map.width, plan_map.height)
        partial_results.update({self.identifier: result})
        return result


class ObstacleDensity(Metric):
    def __init__(self):
        super().__init__("_obstacle_density")

    def evaluate(self, data: Plan, partial_results: dict[str, Any]) -> float:
        super().evaluate(data, partial_results)
        plan_map = data.scenario.map
        size = plan_map.width * plan_map.height

        if size == 0:
            return 0

        result = len(plan_map.obstacles) / size
        partial_results.update({self.identifier: result})
        return result


class AverageSumOfCosts(AggregatePlanMetric):

    def __init__(self):
        super().__init__("_avg_sum_of_costs")

    def evaluate(self, data: list[Plan], partial_results: dict[str, Any]) -> float:
        plans_num = len(data)
        result = 0

        if plans_num != 0:
            total_sum_of_costs = 0
            for index, plan in enumerate(data, 1):
                total_sum_of_costs += SumOfCosts().evaluate(plan, partial_results["_plans"]["_plan_" + str(index)])

            return total_sum_of_costs / plans_num

        partial_results.update({self.identifier: result})
        return result


class VertexConflicts(Metric):

    def __init__(self):
        super().__init__("_vertex_conflicts")

    def evaluate(self, data: Plan, partial_results: dict[str, Any]):
        super().evaluate(data, partial_results)


        result =

        partial_results.update({self.identifier: result})
