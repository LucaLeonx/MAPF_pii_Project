from abc import ABC
from typing import Any

from mapfbench.description import Plan, Action
from mapfbench.metrics.metric_helpers import Metric, MultipleMetric, NumberOfAgents, MapDimensions, ObstacleDensity, \
    Makespan, \
    SumOfCosts, AverageMakespan, NumberOfPlans, AverageSumOfCosts
from mapfbench.utils import dict_manipulations
from mapfbench.utils.dict_manipulations import use_readable_prefixes

default_plan_metrics = [NumberOfAgents(), MapDimensions(), ObstacleDensity(), Makespan(),
                        SumOfCosts()]

default_agent_metrics = []

default_aggregate_metrics = []


class Results(ABC):

    def __init__(self, data: Any, metrics: list[Metric], results_dict: dict[str, Any] = None):
        self._data = data
        self._metrics = metrics
        # Attention: this must be a pass by reference to allow
        # communication between different classes
        self._results = results_dict if results_dict is not None else {}
        self._label_associations = {}

        for metric in self._metrics:
            self._label_associations.update({metric.identifier, metric.label})

    @property
    def data(self) -> Any:
        return self.data

    @property
    def results_dict(self):
        return self._results

    @property
    def results(self):
        return dict_manipulations.recursive_replace_from_prefixes(self._results, self._label_associations)

    @property
    def metrics(self):
        return self._metrics

    def evaluate(self):
        self._results.update({"_data": self._metrics})
        for metric in self._metrics:
            metric.evaluate(self._results)
        del self._results["_data"]


class AgentResults(Results):
    def __init__(self, actions: list[Action], metrics: list[Metric] = None):
        super().__init__(actions, metrics)


class PlanResults(Results):
    def __init__(self, plan: Plan, metrics: list[Metric] = None):
        super().__init__(plan, metrics)
        self._agents_results = []
        self._results.update({"_agents": {}})
        for agent, agent_plan in plan.agent_plans.items():
            agent_key = "_agent_" + str(agent.id)
            self._results["_agents"].update({agent_key: {}})






class PlanResults:
    def __init__(self, plan: Plan, metrics: list[Metric] = None, results_dict: dict[str, Any] = None):
        self._plan = plan
        self._metrics = metrics if metrics is not None else default_plan_metrics
        self._results_dict = {} if results_dict is None else results_dict

    @property
    def plan(self) -> Plan:
        return self._plan

    @property
    def metrics(self) -> list[Metric]:
        return self._metrics

    @property
    def results(self) -> dict[str, Any]:
        self._compute_results()
        return use_readable_prefixes(self._results_dict)

    @property
    def results_dict(self) -> dict[str, Any]:
        self._compute_results()
        return self._results_dict

    def _compute_results(self):
        all_metrics = MultipleMetric("test", metrics=self.metrics)
        all_metrics.evaluate(self.plan, self._results_dict)


class MultiplePlansResults:
    def __init__(self, plans: list[Plan], metrics: list[Metric] = None, results_dict: dict[str, Any] = None):
        self._results_dict = {} if results_dict is None else results_dict
        self._metrics = [NumberOfPlans(), AverageMakespan(), AverageSumOfCosts()]
        if metrics is not None:
            self._metrics += metrics
        self._plans = plans
        self._plan_results = []

    @property
    def metrics(self) -> list[Metric]:
        return self._metrics

    @property
    def results(self) -> dict[str, Any]:
        self._compute_results()
        return use_readable_prefixes(self._results_dict)

    @property
    def results_dict(self) -> dict[str, Any]:
        self._compute_results()
        return self._results_dict

    @property
    def per_plan_results(self):
        self._compute_results()
        return self._plan_results

    def _compute_results(self):
        all_metrics = MultipleMetric("aggregate", metrics=self.metrics)
        all_metrics.evaluate(self._plans, self._results_dict)
        if len(self._plan_results) == 0:
            for plan, test_dict in zip(self._plans, self._results_dict["_plans"].values()):
                self._plan_results.append(PlanResults(plan, results_dict=test_dict))
