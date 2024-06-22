# Parallel benchmark execution

MAPFBench allows to run tests in parallel, to speed up benchmark running.
There are two possibilities for parallel benchmark runs:

- Analyzing the scenarios in parallel, using a local pool of processes
- Use a benchmark server to distribute the tests to executors 
  over the network

Both methods are implemented by the cbs_parallel and cbs_client
solvers in the docs\examples\solvers directory

## Parallelizer

The Parallelizer runs a list of Scenarios in parallel.
Each scenario is processed by a solving function, which outputs the
corresponding plans in an AggregateResultsPlan class.

```python
def main(number_of_plans=8):
    # Scenarios imports
    scenarios = import_scenarios("../../maps/arena.map.scen")
    parallel = Parallelizer(process_scenario)

    results = parallel.run_tests(scenarios[:number_of_plans])
    results.evaluate()
    export_results_to_csv(results, "metrics")
    export_plans(results, filename="results")
```

It is possible to adjust the number of processes used by the pool 
during the creation of the parallelizer. Keep in mind that, especially
if there are many long running tests, that increasing the number of
processes may not lead to an increase in performance

```python
    parallel = Parallelizer(process_scenario, processes=6)
```

After that the results can be processed. The process_scenario function is the same
used in the basic cbs solver, just changed to return directly the plan.

To run the parallel solver:

```shell
    python cbs_parallel.py
```

## Benchmark server

It is possible to start a preconfigured server from the command line,
just passing as input the file with the scenarios to run.
For instance, if we use those available in the docs/examples/maps folder,
we can run them with the command:

```shell
    mapfbench-run arena.map.scen
```

After starting the server, we can let one or more client connect to it,
request test scenarios and solve them:

```shell
    python cbs_client.py
```

The structure of the solver program uses the BenchmarkClient class
to request test instances and process them. When the TestsFinishedException
is thrown, the solver knows that all the tests have been assigned to a solver,
so it can stop requesting them.

```python
def main():
    # Just process the tests arriving from the server

    client = BenchmarkClient()

    try:
        client.start()
        while True:
            scenario = client.request_scenario()
            print("Scenario requested")
            recorder = process_scenario(scenario)
            client.submit_plan(recorder)
            print("    Scenario submitted")
    except TestsFinishedException:
        print("Tests finished")
```

Two or more solvers can be started in parallel to speed up the execution of tests.

