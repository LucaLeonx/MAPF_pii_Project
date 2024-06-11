# Format of the tests

MAPFBench stores the information about a single test 
in the class TestDescription. After retrieving a test
from a BenchmarkInspector, it is possible to retrieve 
the corresponding description with:

```{python}
test = benchmark_inspector.request_random_test()
test.test_description   # TestDescription 
```
This class is characterized by the following properties:

- A unique name for identification: `test.name`
- A `Graph`, representing the map used for the benchmark: `test.graph`
- A list of entities, representing the elements involved in the benchmark: agents, objectives, and obstacles: `test.entities`

Always keep in mind that all the attributes describing
the tests or the benchmarks are read_only

## The _Graph_ class

The `Graph` class represents a graph with directed, weighted graph.
Its `Node`s are uniquely identified by a non-negative integer index.

They are accessible with the property `graph.nodes`;
To access the index of a node you can use `node.index`.

The `Edge`s of the graph can be retrieved with `graph.edges`
Edges attributes are:
- The starting node: `edge.start_node`
- The ending node: `edge.end_node`
- The weight: `edge.weight`

It is possible to retrieve the nodes adjacent to one of the graph
using the method `get_adjacent_nodes()`

There are other useful subclasses of Graph:
- `UndirectedGraph`, representing an undirected graph. 
It provides the property `graph.undirected_edges` to retrieve only
undirected edges (without listing an edge twice)
- `GridGraph`, an undirected graph where the nodes are arranged 
to form a grid, and the weight of each edge is 1.

An important property of `GridGraph`s is that nodes can be referenced
using cartesian coordinates as well[^cantor]. The coordinates must be non-negative
integers.

For instance, the cell in the following grid corresponds to `Node(coords=(2, 3))`
It is possible to access the coordinates corresponding to a node with
`node.x` and `node.y`.

Moreover, the dimensions of the grid can be retrieved using `grid.rows` and `grid.cols`

[^cantor] Actually, every `Node` instance, regardless of the kind of graph used,
is associated to a cartesian point. The implementation uses the [Cantor pairing function](https://en.wikipedia.org/wiki/Pairing_function#Cantor_pairing_function)

## Entities

In MAPFbench, an _entity_ is any object which occupies a node on the map
The attributes common to any _entity_ are:
- Its name, which identifies an entity within a test: `entity.name`
- An optional `Node` reference for the starting position: `entity.start_position`

The entities available in a test can be of three kinds:
- Agents, which have an additional, required attribute `objective_name`, which
identifies the objective which they must reach
- Objectives
- Obstacles

It is possible to obtain the list of entities of each category 
using the getters `test.agents`, `test.objectives`, `test.description`

## Code documentation

For a more detailed description of the classes used for the description of 
the tests, see the relevant [code documentation](../source/mapfbench.description)

