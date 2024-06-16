from typing import Any


class Result:
    def __init__(self, data, partial_results: dict[str, Any] = None):
        self._data = data
        self._partial_results = partial_results if partial_results is not None else {}

    @staticmethod
    def calculate(data, metrics: list[Metric]):
        partial_results = {}
        for metric in metrics:
            metric.evaluate(data, partial_results)

    # TODO add results depth
    def to_dict(self, use_labels: bool = False, results_depth: int = 0) -> dict:
        if use_labels:
            return {entry.value[1]: entry.value[0] for entry in self._partial_results.values()}
        else:
            return {entry[0]: entry[1][0] for entry in self._partial_results.items()}

