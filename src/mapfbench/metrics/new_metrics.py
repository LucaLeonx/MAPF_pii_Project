from abc import ABC, abstractmethod
from typing import Any, Tuple, Union, Callable

import numpy as np

from mapfbench.metrics.new_results import Results


class Metric(ABC):
    def __init__(self, identifier: str, label: str, anonymous: bool = False):
        self._identifier = identifier
        self._label = label
        self._anonymous = anonymous

    @property
    def identifier(self):
        return self._identifier

    @property
    def label(self):
        return self._label

    def evaluate(self, results: Results) -> Tuple[float, float]:
        if self.identifier in results.results_dict:
            return results.results_dict[self.identifier]

        result = self._evaluation_function(results)

        if not self._anonymous:
            results.add_metric(self)
            results.results_dict.update({self.identifier: result})
        return result

    def __eq__(self, other):
        if isinstance(other, Metric):
            return self.identifier == other.identifier

    def __hash__(self) -> int:
        return hash(self.identifier)

    @abstractmethod
    def _evaluation_function(self, results: Results) -> Any:
        pass


class ListMetric(Metric):
    def __init__(self, metric: Metric, anonymous=True):
        actual_identifier, actual_label = _use_default_if_none("_list", metric.identifier, metric.label)
        super().__init__(actual_identifier, actual_label, anonymous)
        self._metric = metric

    def _evaluation_function(self, results: Results) -> list[Any]:
        listed_results = []
        for partial_result in results.inner_results:
            listed_results.append(self._metric.evaluate(partial_result))

        return listed_results


class AggregateMetric(Metric):
    def __init__(self, metric: Metric,
                 data_list: str,
                 aggregation_function: Callable[[Any], Any],
                 prefix: str,
                 identifier: str = None, label: str = None,
                 anonymous: bool = False):
        actual_identifier, actual_label = _use_default_if_none(prefix, identifier, label, metric)
        super().__init__(actual_identifier, actual_label, anonymous)
        self._data_list = data_list
        self._aggregation_function = aggregation_function
        self._metric = metric

    def _evaluation_function(self, results: Results):
        values = ListMetric(self._metric).evaluate(partial_results[self._data_list])
        return self._aggregation_function(values)


class SumMetric(AggregateMetric):
    def __init__(self, metric: Metric, data_list: str, identifier: str = None, label: str = None):
        super().__init__(metric, data_list, lambda data: sum(not_none(data)), "_sum",
                         identifier, label)


class AverageMetric(AggregateMetric):
    def __init__(self, metric: Metric, data_list: str, identifier: str = None, label: str = None):
        super().__init__(metric, data_list, avg, "_avg",
                         identifier, label)


class MaxMetric(AggregateMetric):
    def __init__(self, metric: Metric, data_list: str, identifier: str = None, label: str = None):
        super().__init__(metric, data_list, lambda data: max(not_none(data)), "_max",
                         identifier, label)


class GetterMetric(Metric):
    def __init__(self, identifier: str, label: str, name: Union[str, property]):
        super().__init__(identifier, label)
        self._name = name

    def _evaluation_function(self, results: Results) -> Any:
        data = results.data

        if isinstance(self._name, str):
            return data.metadata.get(self._name, None)
        else:
            return self._name.fget(data)


# TODO add manhattan distance and other custom distances
def euclidean_distance(a: np.array, b: np.array):
    return np.linalg.norm(a - b)


# Just an alias to the function, for convenience
euclidean = euclidean_distance


def _use_default_if_none(prefix: str, identifier, label, metric: Metric) -> Tuple[str, str]:
    actual_identifier = prefix + metric.identifier if identifier is None else identifier
    actual_label = prefix[1:].capitalize() + " " + metric.label if label is None else label
    return actual_identifier, actual_label


def not_none(data: list[Any]) -> list[Any]:
    return [x for x in data if x is not None]


def avg(data: list[Any]) -> Any:
    data = not_none(data)
    if len(data) == 0:
        return 0
    else:
        return sum(data) / len(data)
