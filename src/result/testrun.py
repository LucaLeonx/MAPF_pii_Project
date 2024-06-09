from typing import Any, Dict

from description.benchmarkdescription import TestDescription, BenchmarkDescription
from result.action import Action


class TestRun(TestDescription):

    def __init__(self, test_description, action_list, is_solved, time_elapsed=None, memory_usage=None):
        super().__init__(test_description.name, test_description.graph, test_description.entities)
        self._test_description = test_description
        self._action_list = action_list
        self._is_solved = is_solved
        self._time_elapsed = time_elapsed  # In ms
        self._memory_usage = memory_usage  # In Kb

    @property
    def test_description(self) -> TestDescription:
        return self._test_description

    @property
    def action_list(self) -> list[Action]:
        return self._action_list

    @property
    def time_elapsed(self):
        return self._time_elapsed

    @property
    def memory_usage(self):
        return self._memory_usage

    @property
    def is_solved(self) -> bool:
        return self._is_solved

    def to_dict(self) -> dict[str, Any]:
        dictionary = {"test_description": self.test_description.to_dict(),
                "action_list": [action.to_dict() for action in self.action_list],
                "is_solved": self.is_solved}

        if self.time_elapsed is not None:
            dictionary.update({"time_elapsed": self.time_elapsed})
        if self.memory_usage is not None:
            dictionary.update({"memory_usage": self.memory_usage})

        return dictionary

    @staticmethod
    def from_dict(dictionary):
        time_elapsed = None
        memory_usage = None
        if "time_elapsed" in dictionary:
            time_elapsed = dictionary["time_elapsed"]
        if "memory_usage" in dictionary:
            memory_usage = dictionary["memory_usage"]

        return TestRun(TestDescription.from_dict(dictionary["test_description"]),
                       [Action.from_dict(action) for action in dictionary["action_list"]],
                       dictionary["is_solved"],
                       time_elapsed=time_elapsed,
                       memory_usage=memory_usage)


class BenchmarkRun(BenchmarkDescription):
    def __init__(self, benchmark_description, results: dict[str, list[TestRun]]):
        super().__init__(benchmark_description.name, benchmark_description.test_occurrences)
        self._benchmark_description = benchmark_description
        self._results = results

    @property
    def benchmark_description(self):
        return self._benchmark_description

    @property
    def results(self):
        return self._results

    @property
    def result_list(self):
        return sum(self.results.values(), [])

    def to_dict(self) -> dict[str, Any]:
        dictionary = super().to_dict()
        test_results = {}
        for test_name, test_iterations in self.results.items():
            test_results.update({test_name: [test_run.to_dict()["action_list"] for test_run in test_iterations]})

        dictionary["results"] = test_results
        return dictionary

    @staticmethod
    def from_dict(dictionary: Dict[str, Any]):
        benchmark_description = BenchmarkDescription.from_dict(dictionary)
        results = {}
        for test_name, test_run_list in dictionary["results"].items():
            results.update({test_name: [TestRun.from_dict(test_run) for test_run in test_run_list]})

        return BenchmarkRun(benchmark_description, results)
