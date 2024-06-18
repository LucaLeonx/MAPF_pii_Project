import json
from abc import ABC
from typing import Any

from mapfbench.description import Action, Plan, Agent
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
    def __init__(self, data: Any, metrics: list[Metric] = None, ):
        self._data = data

        self._metrics = metrics if metrics is None else []
        self._label_associations = {}

        for metric in self._metrics:
            self.add_metric(metric)

        self._results = {}
        self._inner_results = []

    @property
    def data(self) -> Any:
        return self.data

    @property
    def results_dict(self):
        return self._results

    @property
    def results(self):
        return dict_manipulations.replace_from_prefixes(self._results, associations)

    @property
    def metrics(self):
        return self._metrics

    def add_metric(self, metric: Metric):
        self._metrics.append(metric)
        self._label_associations.update({metric.identifier: metric.label})

    @property
    def inner_results(self):
        return self._inner_results

    def evaluate(self):
        for metric in self._metrics:
            metric.evaluate(self)


class AgentResults(Results):
    def __init__(self, actions: tuple[Agent, list[Action]], metrics: list[Metric] = None):
        actual_metrics = metrics if metrics is not None else default_agent_metrics
        super().__init__(actions, actual_metrics)


class PlanResults(Results):
    def __init__(self, plan: Plan, metrics: list[Metric] = None):
        actual_metrics = metrics if metrics is not None else default_agent_metrics
        super().__init__(plan, actual_metrics)
        for agent_plan in plan.agent_plans.items():
            self._inner_results.append(AgentResults(agent_plan, [AgentId()]))


class AggregatePlanResults(Results):
    def __init__(self, plans: list[Plan], metrics: list[Metric] = None):
        actual_metrics = metrics if metrics is not None else default_aggregate_metrics
        super().__init__(plans, actual_metrics)
        for plan in plans:
            self._inner_results.append(PlanResults(plan, [Bucket()]))