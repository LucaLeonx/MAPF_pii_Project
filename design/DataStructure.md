# Data Structure Reference

L'uso delle strutture dati avverrà tramite la Standard Template Library che introduce 
i Containers che sono quanto di più vicino ai Generics&Collection di Java.
Si possono trovare informazioni qui: https://github.com/qqqil/ebooks/blob/master/c%2B%2B/the_c_standard_library_2nd_edition.pdf

<img title="Containers" alt="" src="Cpp Containers.jpg">
Notare che a differenza dalle Collection di java è che qui i diversi oggetti non sono sottoclasse l'uno dell'altra, ma sono oggetti 
profondamente diversi, questo non preclude l'esistenza di un iteratore generale capace di lavorare con tutti.

## Strutture/optional usati
Set<> -> set/multiset(più occorrenze concesse)
List ->  


- Class Node    
    +getAdjacentNodes(): Set<int> 
- Class Graph   
    +Graph(nodeSet: Set<Node>)    
    +getNode(position: int): Option<Node>
- Class GraphFactory
    +createDirectedGraph(nodeSet: Set<Node>): Graph
    +createUndirectedGraph(nodeSet: Set<Node): Graph
- Class EntityList
    List<Entity>
    +getAgentsList() : List<Agents>
    +getObstaclesList() : List<Obstacle>
    +getObjectiveList() : List<Objective>
- Class Entity
    -position: Option<int>
    +getPosition(): Option<int>
- Class Test
    -entitiesInfo: List<Entity>
- Class Benchmark
    -tests: List<Test>
    -Benchmark(name: String, description: String: tests: List<Tests>)
- TestRun
    -metrics: List<Metric>
    -actionList: List<Action>
    +getActionList() : List<Action>
    +getMetrics() : List<Metric>


