# Format of the tests

Internally, MAPDbench uses its own formats to store the test instances.
It is based on the following core components

## GridMap

This class represents a 2D Map. Its contents are either free cells or obstacle cells.

The dimensions of the grid can be obtained with:

```python
grid.width, grid.height
```

It is possible to get the list of free and occupied positions on the map as


```python
grid.free_positions
grid.obstacles
```

These positions are provided as a NumPy matrix, with rows representing the positions (length 2 arrays:
the first element is the x of the position, the second the y). The way to access position is similar to using
a Python native list of lists.
The coordinates follow the conventions of the .map file format. The upper-left corner is at coordinates
(0, 0); the x increases horizontally, from left to right; the y increases vertically, from top to bottom.

## Agent

An Agent is identified by its id, start position and objective positions.

To access the properties of an agent

```python

agent.id
agent.start_position
agent.objective_position
```

Positions are supplied as NumPy arrays also in this case

## Scenario

A Scenario represents a MAPF problem instance to solve.
It is characterized by a map and a list of agents in it.

The following can be accessed as:

```python
scenario.map
scenario.agents
```
Additional information about the agents can be obtained as well:

```python
scenario.agents_num
scenario.agents_ids
```

## Plan 

A Plan represents a solution to a MAPF problem instance. It is characterized by the initial scenario
and the actions performed by the agents. 

```python
plan.scenario
plan.actions
```

It is possible to get also the plans for each agent, as a dictionary where
agents are the keys and the values are the lists of actions performed by 
each agent

```python
plan.agent_plans
```

However, it is better to use the other facilities of the library to register the actions in a plan
and calculate the related metrics.


## Code documentation

For a more detailed description of the classes used for the description of 
the tests, see the relevant [code documentation](../source/mapfbench)

