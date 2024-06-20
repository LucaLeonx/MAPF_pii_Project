# Roadmap

## description

1. [ ] Add benchmarks for weighted graphs and 3D graphs
  (represent the positions in the former as single element arrays,
   in the latter as 3-components vectors)
2. [x] Add metadata as dict[str, values] to Scenario and Plan
   - Identifiers start with "_" for private data metrics
3. [ ] Detect moves where start_position = end position and convert to waits

## metrics

Metrics with identifier (str), label (str, human-readable),
function for calculation.

1. Add parallelization for calculations (if necessary)
2. Agent metrics:
    - [x] Distance (Parallel)
    - [ ] Number of Moves (Full)
    - [ ] Number of Waits (Full)
    - [x] Time required (Full)
3. Test metrics
    - [x] Solved
    - [x] Makespan (Parallel)
    - [x] Sum of costs (Full)
    - [x] Running Time (Full)
    - [x] Memory used (Full)
    - [x] Vertex conflicts (Parallel)
    - [x] Edge conflicts (Parallel)
    - [x] Conflicts to add to results
4. Benchmark metrics
    - [x] Average MakeSpan
    - [x] Average SumOfCosts
    - [x] Number of successes (no conflict + solved)
    - [x] Success rate
    - [x] Average running time
    - [x] Average memory consumed

## import/export

1.  [x] Import from .map format of maps
2.  [x] Import from .scen format of scenarios
3.  [x] Export maps to .map
4.  [x] Export scenarios to .scen
5.  [x] Export scenarios, plan, scen to .yaml (with metadata)
6.  [x] Export metrics to .csv
7.  [ ] Export metrics to Pandas Dataframe
8.  [ ] Create new .yaml map and scenario file (with iteration numbers)
9.  [ ] Rename bucket to test number
10. [ ] Aggregate by iteration
11. [ ] Export old map and scenario files in the new format

## instrument

1. [x] Make instrumenter for benchmark
2. [ ] Make benchmark server and parallelized execution
3. [ ] C++ instrumenter

## generator

1. [ ] Generate random instances of maps
   - Vary density of obstacles, various algorithms
    for generation (uniform distribution, clusters, with water)
2. [ ] Generate random scenarios 
   - Vary number of agents and objectives, various algorithms
     for generation (uniform, pretty far)
3. [ ] Introduce water and swamp tiles
4. [ ] Introduce filters to remove swamp and water
5. [ ] Introduce validators for plans (e.g., do not allow diagonal movements, or teleports)

## visualizer

1. [ ] Visualize plans from results
2. [ ] Visualize metrics
