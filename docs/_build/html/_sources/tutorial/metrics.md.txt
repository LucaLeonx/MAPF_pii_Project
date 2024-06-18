# Metrics

After having received all the results from the tests, MAPFBench
elaborates some associated indices. Then they are dumped to
as CSV tables.

For each test iteration, the following metrics are available
- Solved: shows whether a plan has been found for the given test or not
- Number of collisions: cumulative number of vertex and edge conflicts registered in the test
- Sum of costs
- Makespan
- Average cost: average cost of the plans of each agent
- Time elapsed: only if profiling enabled during test (in ms)
- Memory used: only if profiling enabled during test (in kilobytes)


Moreover, the following aggregate metrics are calculated for
multiple iterations of the same test:
- Average Makespan
- Average Sum of Costs
- Number of successes: a test iteration is considered successful if it has been solved and there were no conflicts
- Average running time (in ms)
- Average memory usage (in kilobytes)