# Your first benchmark

## The benchmarking workflow
Running a benchmark in MAPFbench involves 
the following steps:

1. __Importing a benchmark file__. This file is a specially
   formatted .yaml file containing a collection of tests.
   
   Each test represents a MAPF problem instance and includes:
   - A unique, identifying name 
   - A graph
   - A list of entities which need to be considered during
     the benchmark, that is agents, objectives and obstacles

   A benchmark may include more iterations of the same test.

2. __Running the benchmark__. After having imported a benchmark, its tests must be
   submitted to the running programs, and their results collected.

   MAPFBench enables this by employing a client-side architectures:
   there is a central server, the BenchmarkRunner, which
   communicates with programs using a specific component,
   called BenchmarkInspector.

   Programs running MAPF solvers can request tests and submit
   corresponding plans using this object. Moreover, 
   multiple instances of the same program can be run in 
   parallel, in order to finish all tests faster

3. __Calculating metrics__. After having collected all test
   results, MAPFbench elaborates them, determining
   whether there are conflicts in the submitted plans and
   calculating corresponding metrics (e.g. makespan, sum of costs...)

4. __Exporting results__. Both the generated plans and the corresponding
   metrics are exported in files: the former in .yaml format, the latter in a .csv table

## Instrumenting a program

In order to make a program able to communicate with the BenchmarkRunner, we
must instrument it.

:::{warning}
At the moment, it is possible to instruments scripts in Python only
(or, at least, with python bindings)
:::

In the next section, we will try to make a program run a simple benchmark,
available in the `/examples/simple_benchmark.txt` folder of the
[project repository](https://github.com/LucaLeonx/MAPF_pii_Project/tree/main/docs/examples)



where the agent A1 needs to reach the objective T1

First of all, we need to create a BenchmarkInspector.
Inside the main code of the program:

```python
from mapfbench.inspector.benchmarkinspector import BenchmarkInspector

benchmark_inspector = BenchmarkInspector()
```

Then, we need to request a test from the BenchmarkRunner.

```python
test = benchmark_inspector.request_random_test()
```

Now we can access the information about the test.
The MAPFbench library uses its own internal format to
store test data, so you may need to convert it 
to the one used by your program. For this
example test we will skip this passage.

At this point, we wait for the program compute a plan.
Now we need to register the computed plan. Each plan is
composed of two main kinds actions: move and wait.
In order to register them, we write:

```python
test.register_move(1, "A1", Node(coords=(1, 0)))
# or
test.register_wait(1, "A1")
```

where the parameters are:
- timestep at which the action is performed
- The name of the agent performing it ("A1")
- In the case of the move action, we add a Node object,
  representing the position in which the movement ends

We don't need to register the start position of the agents: 
the inspector takes already care of that.

Finally, after having registered all actions, we can submit the result

```python
test.mark_as_solved()
benchmark_inspector.submit_result(test)
```

## Running the benchmark

Now we need to run the benchmark. In order to do this,
we use the library command line utility.

```shell
mapfbench run simple_benchmark.yaml
```

This command will start a BenchmarkRunner which will serve the tests
in the simple_benchmark.yaml file. By default, the BenchmarkRunner 
communicates with the BenchmarkInspectors on localhost, port 9361.

Now we can run or MAPF program and wait for the results.
As soon as the results are received, in the same folder there will be
three new files:
- [timestamp]_SampleBenchmark_results.yaml, containing the plans computed by the program
- [timestamp]_SampleBenchmark_metrics.csv, containing the metrics associated with the plan
- [timestamp]_SampleBenchmark_metrics_aggregate.csv. This file contain aggregate metrics,
calculated on multiple test_runs

The benchmark run is now complete




