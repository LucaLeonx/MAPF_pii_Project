from multiprocessing import Pool
from typing import Callable

from mapfbench.description import Scenario
from mapfbench.instrument import PlanRecorder
from mapfbench.metrics import AggregatePlanResults


class Parallelizer:

    def __init__(self, solver_function: Callable[[Scenario], PlanRecorder], processes: int = 4):
        self._processes = processes
        self._solver_function = solver_function

    def run_tests(self, scenarios: list[Scenario]) -> AggregatePlanResults:
        recorders = []
        with Pool(self._processes) as pool:
            recorders = pool.map(self._solver_function, scenarios)

        plans = [recorder.plan for recorder in recorders]
        return AggregatePlanResults(plans)



