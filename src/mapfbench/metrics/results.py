import json
from abc import ABC
from typing import Any

from mapfbench.description import Action, Plan, Agent
import mapfbench.metrics.metrics as mt

# Attention: import the module this way to avoid ImportErrors due to circular imports

from mapfbench.utils import dict_manipulations


class Results(ABC):
    def __init__(self, data: Any, inner_results: list["Results"] = None):
        self._data = data
        self._label_associations = {}
        self._results = {}
        self._inner_results = [] if inner_results is None else inner_results

    @property
    def data(self) -> Any:
        return self._data

    @property
    def results_dict(self):
        return self._results

    @property
    def results(self):
        return dict_manipulations.replace_from_prefixes(self._results, self._label_associations)

    @property
    def inner_results(self):
        return self._inner_results

    @property
    def label_associations(self):
        return self._label_associations

    def evaluate(self, metrics: list["Metric"] = None):
        for metric in metrics:
            result = metric.evaluate(self)


class AgentResults(Results):
    def __init__(self, actions: tuple[Agent, list[Action]]):
        super().__init__(actions)

    def evaluate(self, metrics: list["Metric"] = None):
        actual_metrics = metrics

        if metrics is None:
            actual_metrics = mt.default_agent_metrics

        super().evaluate(actual_metrics)


class PlanResults(Results):
    def __init__(self, plan: Plan):
        inner_results = []
        for agent_plan in plan.agent_plans.items():
            agent_results = AgentResults(agent_plan)
            agent_results.evaluate([mt.AgentId()])
            inner_results.append(agent_results)

        super().__init__(plan, inner_results)

    def evaluate(self, metrics: list["Metric"] = None):
        actual_metrics = metrics
        if metrics is None:
            actual_metrics = mt.default_plan_metrics

        super().evaluate(actual_metrics)


class AggregatePlanResults(Results):
    def __init__(self, plans: list[Plan]):
        inner_results = []
        for plan in plans:
            plan_results = PlanResults(plan)
            plan_results.evaluate([mt.Bucket(), mt.ScenarioFile(), mt.NumberOfAgents()])
            inner_results.append(plan_results)

        super().__init__(plans, inner_results)

    def evaluate(self, metrics: list["Metric"] = None):
        actual_metrics = metrics

        if metrics is None:
            actual_metrics = mt.default_aggregate_metrics

        super().evaluate(actual_metrics)
