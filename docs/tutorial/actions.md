# Registering actions

During the test, it is possible to register various kinds of actions,
executed by entities. Each action is characterized by:
- The timestep at which it is executed
- The name of the entity executing it
- An optional start or end position of the entity executing it
- An optional additional description of the action

The available actions are of four different kinds:
- Move: the entity moves along one of the edges of the graph
- Wait: the objective waits, remaining in its current position
- Appear: the entity appears in the specified position
- Disappear: the entity disappear from its current position

To register an entity action during a test, the following methods are provided:

// Include code documentation

Moreover, only if working with a GridGraph, the following methods can be used

// Include move_left, right, up, down, methods

## Caveats
- It is not necessary to register the initial position of entities,
as the inspector takes already care of that