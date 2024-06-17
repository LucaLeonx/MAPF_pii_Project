import json
from abc import ABC
from typing import Any

from mapfbench.description import Action, Plan
from mapfbench.metrics.new_metrics import Metric
from mapfbench.metrics.metrics import *
from mapfbench.utils import dict_manipulations

default_agent_metrics = [AgentId(), MaxTime(), Distance()]

default_plan_metrics = [Bucket(), ScenarioFile(), NumberOfAgents(), MapDimensions(), Makespan(), SumOfCosts(),
                        RunningTime(), MemoryUsed()]

default_aggregate_metrics = [AverageMakespan(), AverageSumOfCosts(), NumberOfSuccesses(), SuccessRate(),
                             AverageRunningTime(), AverageSumOfCosts()]


associations = dict_manipulations.get_associations()


class Results(ABC):
    def __init__(self, data: Any, metrics: list[Metric], results_dict: dict[str, Any] = None):
        self._data = data
        self._metrics = metrics
        # Attention: this must be a pass by reference to allow
        # communication between different classes
        self._results = results_dict if results_dict is not None else {}
        self._label_associations = {}
        self._results.update({"_data": self._data})

        for metric in self._metrics:
            self._label_associations.update({metric.identifier: metric.label})

    @property
    def data(self) -> Any:
        return self.data

    @property
    def results_dict(self):
        return self._results

    @property
    def results(self):
        return dict_manipulations.recursive_replace_from_prefixes(self._results, associations)

    @property
    def metrics(self):
        return self._metrics

    def evaluate(self):
        for metric in self._metrics:
            metric.evaluate(self._results)


class PlanResults(Results):
    def __init__(self, plan: Plan, metrics: list[Metric] = None):
        actual_metrics = default_plan_metrics if metrics is None else metrics
        super().__init__(plan, actual_metrics)
        self._results.update({"_agents": {}})
        for agent, agent_plan in plan.agent_plans.items():
            agent_key = "_agent_" + str(agent.id)
            self._results["_agents"].update({agent_key: {"_data": agent_plan}})


    @property
    def per_agent_results(self):
        return self.results["Agents"].values()


class AggregatePlanResults(Results):
    def __init__(self, plans: list[Plan], metrics: list[Metric] = None):
        if metrics is None:
            metrics = default_aggregate_metrics
        super().__init__(plans, metrics)
        self._results.update({"_plans": {}})
        for index, plan in enumerate(plans):
            plan_key = "_plan" + str(index)
            self._results["_plans"].update({plan_key: {"_data": plan}})
            plan_dict = self._results["_plans"][plan_key]
            plan_dict.update({"_agents": {}})
            for agent, agent_plan in plan.agent_plans.items():
                agent_key = "_agent_" + str(agent.id)
                plan_dict["_agents"].update({agent_key: {"_data": agent_plan}})

    @property
    def per_plan_results(self):
        return self.results["Plans"]
