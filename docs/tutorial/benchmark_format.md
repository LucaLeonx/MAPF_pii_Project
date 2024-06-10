# Format of the benchmarks

Benchmarks can be supplied to MAPFBench as .yaml files. 
Their format is conceived to maximize readability and ease of change.
Benchmark example files are available in the docs\examples folder
It is __recommended__ to read them to have an example of
the possible, available formats.

## Fields of benchmark descriptions

The fields of a benchmark file are the following:

- name: Name of the benchmark
- test_occurrences: Specifies the number of iterations of each test that
will be performed during the benchmark
The format is: `name : number_of_iterations`
- tests: The description of each test. 

The fields describing a test are:
- name: Name of the test 
- graph: The graph representing the map. Its format depends on the type:
  - DirectedGraph: the edge list must be supplied in the field edges.
    The format for each edge is the following:
    `[start_node, end_node | weight]`
     For instance `[1, 2 | 3]`.
     The nodes can be specified using their coordinates as well: `[(0, 1), (1, 2) | 3]`
  - UndirectedGraph: The edges follow the same format as DirectedGraph,
    but are treated as undirected edges.
  - GridGraph: It is sufficient to supply only the dimension of the grid,
    in terms of `rows` and `cols`.
- entities: the list of the entities involved in the test. 
There are two possible formats for it:
- Divided in sublists of `agents`, `objectives`, `obstacles`.
Each entity has a `name` and an optional `start_position`. Moreover, for
the agents the `objective_name` must be specified

- Using the field `placement`, to visually represent the position of the entities
on the map. This format can be used only if the map is a GridGraph:
  - Each cell is separated from the others using a vertical bar `|`. 
  - A row is terminated by a double bar `||`
  - Agents are identified by letter A, followed by a progressive number.
    The corresponding objective is identified by T (for Target), followed by the same number
    (e.g., the objective of agent A3 is T3).
  - Obstacles are denoted simply by letter O
  - It is implicitly assumed that the grid is located in the first quadrant of the cartesian plane.
    For instance, the coordinates of the cells in this grid would be the following:
    :::{line-block}
    2 |     |     |     ||
    1 |     |     |  T1 ||
    0 |  A1 |     |     ||
         0     1     2 
    :::
  - It is important to remember the YAML tag `!Map |` at the beginning
    of the grid representation. 
