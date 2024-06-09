from commanddispatcher import CommandDispatcher
from metrics.testMetrics import TestMetrics
from result.testrun import BenchmarkRun


class BenchmarkMetrics(BenchmarkRun):
    def __init__(self, benchmark_run):
        super().__init__(benchmark_run.benchmark_description, benchmark_run.results)
        self._aggregate_metrics = []
        for test_name, test_iterations in benchmark_run.results.items():
            self._aggregate_metrics.append(AggregateMetrics(test_name, test_iterations))

    @property
    def aggregate_metrics(self):
        if not self._aggregate_metrics:
            self.evaluate()

        return self._aggregate_metrics

    def evaluate(self):
        for aggregate_metric in self._aggregate_metrics:
            aggregate_metric.evaluate()

    def to_dict(self):
        return dict((metric.test_name, metric.to_dict()) for metric in self._aggregate_metrics)


class AggregateMetrics:
    def __init__(self, test_name, iterations):
        self._test_name = test_name
        self._iterations = iterations
        self._iterations_metrics = []
        self._aggregate_metrics = {}
        self._calculating_functions = CommandDispatcher(
            {"Iterations number": self._get_iterations_num,
             "Average MakeSpan": self._avg_makespan,
             "Average Sum of Costs": self._avg_sum_of_costs,
             "Number of successes": self._success_num,
             "Success rate": self._success_rate}
        )

    @property
    def test_name(self):
        return self._test_name

    @property
    def iterations(self):
        return self._iterations

    @property
    def iterations_num(self):
        return len(self._iterations)

    @property
    def iterations_metrics(self):
        if not self._iterations_metrics:
            self._generate_test_metrics()

        return self._iterations_metrics

    def to_dict(self):
        if not self._aggregate_metrics:
            self.evaluate()
        dictionary = {"Test name": self._test_name}
        dictionary.update(self._aggregate_metrics)
        return dictionary

    def _generate_test_metrics(self):
        for iteration in self._iterations:
            test_metric = TestMetrics(iteration)
            self._iterations_metrics.append(test_metric)
            test_metric.evaluate()

    def evaluate(self):
        for function in self._calculating_functions.function_names:
            result = self._calculating_functions.execute(function)
            self._aggregate_metrics.update({function: result})

    def _get_iterations_num(self):
        return self.iterations_num

    def _avg_makespan(self):
        return sum([metric.to_dict()["Makespan"] for metric in self.iterations_metrics]) / self.iterations_num

    def _avg_sum_of_costs(self):
        return sum([metric.to_dict()["Sum of Costs"] for metric in self.iterations_metrics]) / self.iterations_num

    def _success_num(self):
        return sum([1 for metric in self.iterations_metrics
                    if metric.to_dict()["Solved"] and
                    metric.to_dict()["Number of collisions"] == 0])

    def _success_rate(self):
        return self._success_num() / self.iterations_num
