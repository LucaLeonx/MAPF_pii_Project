# Format of results

The computed plans for each test of a completed benchmark
are exported to YAML format as well. 

The first part of the generated file contains the benchmark
description, following the conventions detailed in 

In addition, the following fields are present:
- results: provides a list of the plans for each test.
The plans are presented with:
  - test_name
  - iteration_number
  - action_list: list of actions executed during the test

- conflicts: list of conflicts for each iteration. Only
iterations with at least one conflicts are listed