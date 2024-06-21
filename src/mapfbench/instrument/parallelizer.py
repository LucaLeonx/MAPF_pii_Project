from multiprocessing import Pool
from typing import Callable

from mapfbench.description import Scenario, Plan
from mapfbench.metrics import AggregatePlanResults


class Parallelizer:

    def __init__(self, solver_function: Callable[[Scenario], Plan], processes: int = 4):
        self._processes = processes
        self._solver_function = solver_function

    def run_tests(self, scenarios: list[Scenario]) -> AggregatePlanResults:
        plans = []
        try:
            with Pool(self._processes) as pool:
                plans = pool.map(self._solver_function, scenarios)
        except KeyboardInterrupt:
            pool.terminate()
            pool.join()
            raise KeyboardInterrupt()

        return AggregatePlanResults(plans)



