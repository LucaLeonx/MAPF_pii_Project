from typing import Any

from mapfbench.description import Plan
from mapfbench.metrics.metric import Metric, MultipleMetric, NumberOfAgents, MapDimensions, ObstacleDensity, Makespan, \
    SumOfCosts, AverageMakespan, NumberOfPlans, AverageSumOfCosts
from mapfbench.utils.dict_manipulations import use_readable_prefixes


class PlanResults:

    def __init__(self, plan: Plan, metrics: list[Metric] = None, results_dict: dict[str, Any] = None):
        self._plan = plan
        self._metrics = [NumberOfAgents(), MapDimensions(), ObstacleDensity(), Makespan(),
                         SumOfCosts()]
        if metrics is not None:
            self._metrics += metrics
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

