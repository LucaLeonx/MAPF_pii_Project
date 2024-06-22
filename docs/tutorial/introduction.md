# Your first benchmark

## The benchmarking workflow
Running a benchmark in MAPFbench involves 
the following steps:

1. __Importing benchmark files__. MAPFBench can import .map and .scen files
   with the format detailed by [Nathan Sturtenvant on movingai.com](https://movingai.com/benchmarks/formats.html)
   
   Each benchmark is composed of several scenarios, distinguished by a
   "bucket" number. A scenario includes a Map,
   and a certain number of agents, along with their starts positions and
   objective positions. 

   Sample files can be found under docs\examples\maps in the project repository.
   
   MAPFBench is able to directly import scenarios with their maps, provided that the
   path listed in the .scen files. Paths are treated as relative to the scenario file

2. __Running the benchmark__. After having imported a benchmark, its tests must be
   submitted to the running programs, and their results collected.

   This phase requires the conversion of the scenario data in the format used 
   by the solver. 

3. __Calculating metrics__. After having collected all test
   results, MAPFbench elaborates them, determining
   whether there are conflicts in the submitted plans and
   calculating corresponding metrics (e.g. makespan, sum of costs...)

4. __Exporting results__. The computed plans, along with metrics and conflicts,
   can be exported later to a .yaml file. Moreover, numerical indices can be
   exported directly to .csv files

## Instrumenting a program

In order to make a program able to communicate with the BenchmarkRunner, we
must instrument it.

:::{warning}
At the moment, it is possible to instruments scripts in Python only
(or, at least, with python bindings)
:::

In the next section, we will try to make a program run a simple benchmark.
The code we will use is available in the `/examples/solvers/cbs` folder of the
[project repository](https://github.com/LucaLeonx/MAPF_pii_Project/tree/main/docs/examples)

We recommend to download the entire `examples.zip` directory to test it.

Opening the `cbs.py` file, we see the following main() method
```python
def main(number_of_plans=8):
    # Scenarios imports
    scenarios = import_scenarios("../../maps/arena.map.scen")

    # Last scenarios are a bit long to run
    scenarios = scenarios[:number_of_plans]
    computed_plans = []

    ## Scenarios processing
    for scenario in scenarios:
        plan = process_scenario(scenario)
        computed_plans.append(plan)


    # Metrics calculations and results exports
    results = AggregatePlanResults(computed_plans)
    results.evaluate()
    export_results_to_csv(results, "metrics")
    export_plans(results, filename="results")
```

This method performs the import of scenarios and export of results.
Let's see how each scenario is processed in the `process_scenario()` method:

```python
def process_scenario(scenario):
    # Convert scenario data in the format accepted by the solver

    map_scheme = scenario.map
    dimensions = [map_scheme.width, map_scheme.height]
    agents = []
    for index, agent in enumerate(scenario.agents, 1):
        agents.append(
            {"name": str(index), "start": tuple(agent.start_position), "goal": tuple(agent.objective_position)})
    obstacles = [tuple(obstacle) for obstacle in map_scheme.obstacles]
    env = Environment(dimensions, agents, obstacles)
    cbs = CBS(env)

    # Profiling and searching solution

    recorder = PlanRecorder(scenario)
    recorder.start_profiling()
    solution = cbs.search()
    recorder.end_profiling()

    # Plan recording, action after action

    if solution:
        for agent_name, agent_moves in solution.items():
            for move in agent_moves:
                recorder.record_move(move["t"], int(agent_name), (move["x"], move["y"]))
        recorder.mark_as_solved()

    return recorder.plan
```

First of all, the method accesses the scenario information and converts them in the
format used by the solver.

At this point, we run the program to compute a plan,
profiling its performance in the meanwhile. This is done by the
PlanRecorder instance created from the scenario.

At the end, we need to record the actions performed as part of the plan
into the recorder and return back to the main method.


## Running the benchmark


Now we can run or MAPF program and wait for the results.

```shell

python cbs.py

```

As soon as the results are received, in the same folder there will be
three new files:
- results.yaml, containing the plans computed by the algorithm for each scenario
- metrics_plans.csv, containing the detailed metrics calculated for each plan
- metrics.csv, containing the aggregate metrics of all plans

The benchmark run is now complete




