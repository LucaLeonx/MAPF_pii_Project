from typing import Any, Optional

import numpy as np

from mapfbench.description import Action, Plan
from mapfbench.metrics.conflict import EdgeConflict, ObstacleConflict, VertexConflict
from mapfbench.metrics.new_metrics import GetterMetric, Metric, euclidean_distance, SumMetric, MaxMetric, AverageMetric, \
    AggregateMetric


class AgentId(Metric):
    def __init__(self):
        super(AgentId, self).__init__("_id", "Id")

    def _evaluation_function(self, partial_results: dict[str, Any]) -> Optional[int]:
        data = partial_results["_data"]
        if len(data) == 0:
            return None
        else:
            return data[0].subject_id


class Distance(Metric):
    def __init__(self):
        super().__init__("_distance", "Distance")

    def _evaluation_function(self, partial_results: dict[str, Any]) -> float:
        data = partial_results["_data"]
        return sum([euclidean_distance(action.end_position, action.start_position) for action in data])


class MaxTime(Metric):
    def __init__(self):
        super().__init__("_max_time", "Max time")

    def _evaluation_function(self, partial_results: dict[str, Any]) -> int:
        data = partial_results["_data"]
        return max([action.timestep for action in data], default=0)


class Bucket(GetterMetric):
    def __init__(self):
        super().__init__("_bucket", "Bucket", "bucket")


class ScenarioFile(GetterMetric):
    def __init__(self):
        super().__init__("_scenario_file", "Scenario File", "filename")


class NumberOfAgents(Metric):
    def __init__(self):
        super().__init__("_num_of_agents", "Number of agents")

    def _evaluation_function(self, partial_results: dict[str, Any]) -> int:
        return partial_results["_data"].scenario.agents_num


class MapDimensions(Metric):
    def __init__(self):
        super().__init__("_num_of_agents", "Number of agents")

    def _evaluation_function(self, partial_results: dict[str, Any]) -> int:
        return partial_results["_data"].scenario.map.dimensions


class ObstacleRate(Metric):
    def __init__(self):
        super().__init__("_num_of_agents", "Number of agents")

    def _evaluation_function(self, partial_results: dict[str, Any]) -> int:
        map_scheme = partial_results["_data"].scenario.map
        return map_scheme.obstacles.shape[0] / (map_scheme.width * map_scheme.height)


class RunningTime(GetterMetric):
    def __init__(self):
        super().__init__("_running_time", "Running Time", "running_time")


class MemoryUsed(GetterMetric):
    def __init__(self):
        super().__init__("_memory_used", "Memory Used", "memory_used")


class Makespan(MaxMetric):
    def __init__(self):
        super().__init__(MaxTime(), "_agents", "_makespan", "Makespan")


class SumOfCosts(SumMetric):
    def __init__(self):
        super().__init__(MaxTime(), "_agents", "_sum_of_costs", "Sum of costs")


class FuelConsumed(SumMetric):
    def __init__(self):
        super().__init__(Distance(), "_agents", "_fuel_consumed", "Fuel consumed", )


class VertexConflicts(Metric):

    def __init__(self):
        super().__init__("_vertex_conflicts", "Vertex conflicts")

    def _evaluation_function(self, partial_results: dict[str, Any]):
        data = partial_results["_data"]
        actions = data.actions

        if len(actions) == 0:
            return []

        timesteps_extractor = np.vectorize(lambda action: action.timestep)
        timesteps = np.unique(timesteps_extractor(actions))

        conflicts = []

        for action in actions:
            if action.end_position.tolist() in data.scenario.map.obstacles.tolist():
                conflicts.append(ObstacleConflict(action.timestep, action.subject_id, action.end_position))

        for timestep in timesteps:
            actions_performed = np.array([action for action in actions if action.timestep == timestep])

            for i in range(actions_performed.shape[0]):  # Avoid listing a conflict twice
                for j in range(i, actions_performed.shape[0]):
                    if np.array_equal(actions_performed[i].end_position, actions_performed[j].end_position) \
                            and actions_performed[i].subject_id != actions_performed[j].subject_id:
                        conflicts.append(VertexConflict(timestep,
                                                        actions_performed[i].subject_id,
                                                        actions_performed[j].subject_id,
                                                        actions_performed[i].end_position))

        return conflicts


class EdgeConflicts(Metric):
    def __init__(self):
        super().__init__("_edge_conflicts", "Edge conflicts")

    def _evaluation_function(self, partial_results: dict[str, Any]):
        data = partial_results["_data"]
        actions = data.actions

        if len(actions) == 0:
            return []

        timesteps_extractor = np.vectorize(lambda action: action.timestep)
        timesteps = np.unique(timesteps_extractor(actions))
        conflicts = []

        for timestep in timesteps:
            actions_performed = np.array([action for action in actions if action.timestep == timestep], dtype=Action)
            for i in range(actions_performed.shape[0]):  # Avoid listing a conflict twice
                for j in range(i + 1, actions_performed.shape[0]):

                    if (actions_performed[i].end_position.tolist() == actions_performed[j].start_position.tolist()
                            and actions_performed[i].start_position.tolist() == actions_performed[
                                j].end_position.tolist()):
                        conflicts.append(EdgeConflict(timestep,
                                                      actions_performed[i].subject_id,
                                                      actions_performed[j].subject_id,
                                                      actions_performed[i].start_position,
                                                      actions_performed[j].start_position))

        return conflicts


class Solved(GetterMetric):
    def __init__(self):
        super().__init__("_solved", "Solved", "solved")


class Success(Metric):

    def __init__(self):
        super().__init__("_success", "Success")

    def _evaluation_function(self, partial_results: dict[str, Any]) -> Any:
        conflicts = EdgeConflicts().evaluate(partial_results) + VertexConflicts().evaluate(partial_results)
        return Solved().evaluate(partial_results) and len(conflicts) == 0


class AverageRunningTime(AverageMetric):
    def __init__(self):
        super().__init__(RunningTime(), "_plans")


class AverageMemoryUsed(AverageMetric):
    def __init__(self):
        super().__init__(MemoryUsed(), "_plans")


class AverageMakespan(AverageMetric):
    def __init__(self):
        super().__init__(Makespan(), "_plans")


class AverageSumOfCosts(AverageMetric):
    def __init__(self):
        super().__init__(SumOfCosts(), "_plans")


class AverageFuelConsumed(AverageMetric):
    def __init__(self):
        super().__init__(FuelConsumed(), "_plans")


class NumberOfSuccesses(AggregateMetric):
    def __init__(self):
        super().__init__(Success(), "_plans", lambda data: len(list(filter(None, data))), prefix="_num",
                         identifier="_num_successes", label="Number of Successes", anonymous=False)


class SuccessRate(Metric):
    def __init__(self):
        super().__init__("_success_rate", "Success rate")

    def _evaluation_function(self, partial_results):
        data = partial_results["_data"]

        if len(data) == 0:
            return 0

        return NumberOfSuccesses().evaluate(partial_results) / len(data)
