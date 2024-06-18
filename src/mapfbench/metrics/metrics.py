from typing import Any, Optional

import numpy as np

from mapfbench.description import Action
from mapfbench.metrics.conflict import EdgeConflict, ObstacleConflict, VertexConflict
import mapfbench.metrics.metrics_generation as mtdef
import mapfbench.metrics.results as rs


class AgentId(mtdef.Metric):
    def __init__(self):
        super().__init__("_id", "Id")

    def _evaluation_function(self, results: "Results") -> Optional[int]:
        return results.data[0].id


class Distance(mtdef.Metric):
    def __init__(self):
        super().__init__("_distance", "Distance")

    def _evaluation_function(self, results: "Results") -> float:
        data = results.data[1]
        return sum([mtdef.euclidean_distance(action.end_position, action.start_position) for action in data])


class MaxTime(mtdef.Metric):
    def __init__(self):
        super().__init__("_max_time", "Max time")

    def _evaluation_function(self, results: "Results") -> int:
        data = results.data[1]
        return max([action.timestep for action in data], default=0)


class Bucket(mtdef.GetterMetric):
    def __init__(self):
        super().__init__("_bucket", "Bucket", "bucket")


class ScenarioFile(mtdef.GetterMetric):
    def __init__(self):
        super().__init__("_scenario_file", "Scenario File", "filename")


class NumberOfAgents(mtdef.Metric):
    def __init__(self):
        super().__init__("_num_of_agents", "Number of agents")

    def _evaluation_function(self, results: "Results") -> int:
        return results.data.scenario.agents_num


class MapDimensions(mtdef.Metric):
    def __init__(self):
        super().__init__("_map_dimensions", "Map dimensions")

    def _evaluation_function(self, results: "Results") -> int:
        return results.data.scenario.map.dimensions


class ObstacleRate(mtdef.Metric):
    def __init__(self):
        super().__init__("_obstacle_rate", "Obstacle rate")

    def _evaluation_function(self, results: "Results") -> int:
        map_scheme = results.data.scenario.map
        return map_scheme.obstacles.shape[0] / (map_scheme.width * map_scheme.height)


class RunningTime(mtdef.GetterMetric):
    def __init__(self):
        super().__init__("_running_time", "Running Time (ms)", "running_time")


class MemoryUsed(mtdef.GetterMetric):
    def __init__(self):
        super().__init__("_memory_used", "Memory Used (Kb)", "memory_used")


class Makespan(mtdef.SumMetric):
    def __init__(self):
        super().__init__(MaxTime(), "_makespan", "Makespan")


class SumOfCosts(mtdef.SumMetric):
    def __init__(self):
        super().__init__(MaxTime(), "_sum_of_costs", "Sum of costs")


class FuelConsumed(mtdef.SumMetric):
    def __init__(self):
        super().__init__(Distance(), "_fuel_consumed", "Fuel consumed", )


class VertexConflicts(mtdef.Metric):

    def __init__(self):
        super().__init__("_vertex_conflicts", "Vertex conflicts")

    def _evaluation_function(self, results: "Results"):
        data = results.data
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

        return [str(conflict) for conflict in conflicts]


class EdgeConflicts(mtdef.Metric):
    def __init__(self):
        super().__init__("_edge_conflicts", "Edge conflicts")

    def _evaluation_function(self, results: "Results"):
        data = results.data
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

        return [str(conflict) for conflict in conflicts]


class NumberOfEdgeConflicts(mtdef.Metric):

    def __init__(self):
        super().__init__("_number_of_edge_conflicts", "Number of edge conflicts")

    def _evaluation_function(self, results: "Results"):
        conflicts = EdgeConflicts().evaluate(results)
        return len(conflicts)


class NumberOfVertexConflicts(mtdef.Metric):
    def __init__(self):
        super().__init__("_number_of_vertex_conflicts", "Number of vertex conflicts")

    def _evaluation_function(self, results: "Results"):
        conflicts = VertexConflicts().evaluate(results)
        return len(conflicts)


class Solved(mtdef.GetterMetric):
    def __init__(self):
        super().__init__("_solved", "Solved", "solved")


class Success(mtdef.Metric):

    def __init__(self):
        super().__init__("_success", "Success")

    def _evaluation_function(self, results: "Results") -> Any:
        vertex_conflicts = NumberOfVertexConflicts().evaluate(results)
        edge_conflicts = NumberOfEdgeConflicts().evaluate(results)
        conflicts_num = vertex_conflicts + edge_conflicts
        return Solved().evaluate(results) and conflicts_num == 0


class NumberOfScenarios(mtdef.Metric):
    def __init__(self):
        super().__init__("_number_of_scenarios", "Number of Scenarios")

    def _evaluation_function(self, results: "Results") -> Any:
        return len(results.data)


class AverageRunningTime(mtdef.AverageMetric):
    def __init__(self):
        super().__init__(RunningTime())


class AverageMemoryUsed(mtdef.AverageMetric):
    def __init__(self):
        super().__init__(MemoryUsed())


class AverageMakespan(mtdef.AverageMetric):
    def __init__(self):
        super().__init__(Makespan())


class AverageSumOfCosts(mtdef.AverageMetric):
    def __init__(self):
        super().__init__(SumOfCosts())


class AverageFuelConsumed(mtdef.AverageMetric):
    def __init__(self):
        super().__init__(FuelConsumed())


class NumberOfSuccesses(mtdef.AggregateMetric):
    def __init__(self):
        super().__init__(Success(), lambda data: len(list(filter(None, data))), prefix="_num",
                         identifier="_num_successes", label="Number of Successes", anonymous=False)


class SuccessRate(mtdef.Metric):
    def __init__(self):
        super().__init__("_success_rate", "Success rate")

    def _evaluation_function(self, results):
        data = results.data

        if len(data) == 0:
            return 0

        return NumberOfSuccesses().evaluate(results) / len(data)


default_agent_metrics = [AgentId(), MaxTime(), Distance()]

default_plan_metrics = [Bucket(), ScenarioFile(), NumberOfAgents(), MapDimensions(), Makespan(), SumOfCosts(),
                        RunningTime(), MemoryUsed(), NumberOfVertexConflicts(), NumberOfEdgeConflicts()]

default_aggregate_metrics = [NumberOfScenarios(), AverageMakespan(), AverageSumOfCosts(), NumberOfSuccesses(),
                             SuccessRate(), AverageRunningTime(), AverageMemoryUsed()]
