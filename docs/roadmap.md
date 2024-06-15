# Roadmap

## description

1. [ ] Add benchmarks for weighted graphs and 3D graphs
  (represent the positions in the former as single element arrays,
   in the latter as 3-components vectors)
2. [ ] Add metadata as dict[str, values] to Scenario and Plan
   - Use this also for private metadata (solver, runtime-info).
   - Identifiers start with "_" for private data metrics
3. [ ] Detect moves where start_position = end position and convert to waits

## metrics

Metrics with identifier (str), label (str, human readable),
function for calculation

1. [ ] Parallel, Incremental and Full Test
2. Agent metrics:
    - Distance (Parallel)
    - Number of Moves (Full)
    - Number of Waits (Full)
    - Time required (Full)
3. Test metrics
    - Solved
    - Makespan (Parallel)
    - Sum of costs (Full)
    - Running Time (Full)
    - Memory used (Full)
    - Vertex conflicts (Parallel)
    - Edge conflicts (Parallel)
    - Conflicts to add to results
4. Benchmark metrics
    - Average MakeSpan
    - Average SumOfCosts
    - Number of successes (no conflict + solved)
    - Success rate
    - Average running time
    - Average memory consumed

## import/export

1. [ ] Import from .map format of maps
2. [ ] Import from .scen format of scenarios
3. [ ] Export maps to .map
4. [ ] Export scenarios to .scen
5. [ ] Export scenarios, plan, scen to .yaml (with metadata)
6. [ ] Export metrics to .csv
7. [ ] Export metrics to Pandas Dataframe

## instrument

1. [ ] Make instrumenter for benchmark
2. [ ] Export to file
3. [ ] Make benchmark server

## generator

1. [ ] Generate random instances of maps
   - Vary density of obstacles, various algorithms
    for generation (uniform distribution, clusters, with water)
2. [ ] Generate random scenarios 
   - Vary number of agents and objectives, various algorithms
     for generation (uniform, pretty far)

## visualizer

1. [ ] Visualize plans from results
2. [ ] Visualize metrics
