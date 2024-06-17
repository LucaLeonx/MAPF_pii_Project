from abc import ABC, abstractmethod
from typing import Any, Tuple, Union


class Metric(ABC):
    def __init__(self, identifier: str, label: str):
        self._identifier = identifier
        self._label = label

    @property
    def identifier(self):
        return self._identifier

    @property
    def label(self):
        return self._label

    def evaluate(self, partial_results: dict[str, Any]):
        if self.identifier in partial_results:
            return partial_results[self.identifier]

        result = self._evaluation_function(partial_results)
        partial_results.update({self.identifier: result})

    @abstractmethod
    def _evaluation_function(self, partial_results: dict[str, Any]) -> Any:
        pass


class ListMetric(Metric):
    def __init__(self, metric: Metric, identifier: str = None, label: str = None, ):
        actual_identifier, actual_label = _use_default_if_none("_list_", identifier, label, metric)
        super().__init__(actual_identifier, actual_label)
        self._metric = metric

    def _evaluation_function(self, partial_results: dict[str]) -> list[Any]:
        metrics_list = []
        for inner_dict in partial_results:
            metrics_list.append(self._metric.evaluate(inner_dict))

        return metrics_list


class SumMetric(Metric):
    def __init__(self, identifier: str, label: str, metric: Metric):
        actual_identifier, actual_label = _use_default_if_none("_sum_", identifier, label, metric)
        super().__init__(identifier, label)
        self._summed_metric = metric

    def _evaluation_function(self, partial_results: dict[str, Any]) -> float:
        values = ListMetric(self._summed_metric).evaluate(partial_results)
        not_null = [value for value in values if value is not None]

        return sum(values)


class AverageMetric(Metric):
    def __init__(self, identifier: str, label: str, metric: Metric):
        actual_identifier, actual_label = _use_default_if_none("_avg_", identifier, label, metric)
        super().__init__(identifier, label)
        self._averaged_metric = metric

    def _evaluation_function(self, partial_results: dict[str, Any]) -> float:
        values = ListMetric(self._averaged_metric).evaluate(partial_results)
        not_null = [value for value in values if value is not None]
        if len(not_null) == 0:
            return 0
        else:
            return sum(values) / len(values)


class GetterMetric(Metric):
    def __init__(self, identifier: str, label: str, name: Union[str, property]):
        super().__init__(identifier, label)
        self._name = name

    def _evaluation_function(self, partial_results: dict[str]) -> Any:
        data = partial_results["_data"]

        if isinstance(self._name, str):
            return data.metadata.get(self._name, None)
        else:
            return self._name.fget(data)



def _use_default_if_none(prefix: str, identifier, label, metric: Metric) -> Tuple[str, str]:
    actual_identifier = prefix + metric.identifier if identifier is None else identifier
    actual_label = prefix + metric.label if label is None else label
    return actual_identifier, actual_label
