# Design UML, spiegazione

## Caveat

- Vengono prese come riferimento per le strutture dati le Collections di Java.
  Dovranno essere sostituite con i loro equivalenti in C++
 
## Spiegazioni classi

### Graph e Node, GraphFactory

Rappresenta la mappa come grafo diretto, costituito da Node. Ogni Node è identificato 
univocamente in una mappa dalla sua posizione (un intero), ed ha una lista di adiacenza.
Nodi in mappe diverse possono presentare la stessa posizione.
Si assume che la mappa e i nodi siano immutabili (per modificare una mappa esistente, 
bisogna ricrearla da zero).
La classe GraphFactory semplifica la creazione di grafi di tipo diverso (es. griglie)
    
    _Possibili miglioramenti_: in questa classe e in quelle esterne, per identificare 
    un nodo si fa riferimento direttamente alla sua posizione. Potrebbero esserci
    strategie migliori (usare i puntatori all'oggetto, forse). Inoltre, potrebbe essere utile
    un'implementazione da libreria esterna (es. [Boost Library](https://www.boost.org/doc/libs/1_84_0/libs/graph/doc/adjacency_list.html) )

### Separazione tra definizione ed esecuzione

L'idea alla base di questa architettura è la separazione tra:

- I test case su cui provare gli algoritmi, definiti in maniera generale. Essi risultano sostanzialmente immutabili
- Le classi che restituiscono i risultati dei test. Questi si occuperanno di eseguire
effettivamente l'algoritmo e analizzarne i risultati.

### Entity

Rappresenta un'entità fisica presente sul grafo. È mutabile. 
La loro posizione è opzionale, in quanto potrebbero comparire dopo sulla mappa 
(se si utilizzano azioni AppearAction o DisappearAction)
   
   _Possibili miglioramenti_: Creare due classi separate EntityInfo ed Entity, di cui
   una rappresenta solo le informazioni su un'entità, l'altra serve per simulare
   le sue posizioni dopo le varie azioni. In tale ottica, si potrebbe
   addirittura sostituire la classe Entity con la classe immutabile EntityState,
   che indica lo stato e la posizione di un'entità in un dato istante di tempo; 
   le Action non agirebbero mutando le singole entità, bensì producendo un nuovo EntityState. 
   Si tratta di un approccio più funzionale. EntityState potrebbe anche implementare
   le singole azioni
   Inoltre, la posizione opzionale sarebbe necessaria solo in fase di simulazione,
   potrebbe non essere necessario definire tutte le entità prima del test.

### Test e Benchmark

La classe Test rappresenta un singolo caso di Test. Esso risulta caratterizzato da:
- map, il grafo della mappa del test
- entitiesInfo, una lista delle entità da definire

Un Benchmark non è altro che una collezione di Test

### TestRun

Una TestRun rappresenta l'esecuzione di un caso di Test ed il suo risultato. 
Quest'ultimo è rappresentato da una lista di Action, intraprese dai singoli agenti.
Inoltre, al termine di quest'ultimo, vengono calcolate le metriche definite
dalla classe Metric.
    
    _Possibili Miglioramenti_: 
    - Potrebbe essere necessario ritoccare l'interfaccia nel caso si vogliano eseguire più test
    in parallelo.
    - Fare il profiling dell'esecuzione del codice potrebbe richiedere modificare la 
    classe (forse solo all'interno). Ad ogni modo, fare profiling dei programmi
    dall'esterno è molto complicato, quindi le informazioni che si otterrebbero 
    sarebbero generiche. Librerie utili in tal senso: [EasyProfiler](https://github.com/yse/easy_profiler)
    e [gperftools](https://github.com/gperftools/gperftools)

### Action

Rappresenta una possibile azione eseguita da un'entità. È caratterizzata dal timestep 
in cui avviene e dall'entità cui viene applicata. L'implementazione come classe
astratta è per motivi di riuso, andrebbe bene anche un'interfaccia.

    _Possibili miglioramenti_: implementare una classe ActionList che permetta
    di filtrare le azioni per Entity che le esegue e timestep.

### Metric

Interfaccia astratta che calcola una metrica. Riceve in ingresso da TestRun o BenchmarkRun 
tutte le informazioni necessarie e restituisce il risultato aggregato. La scelta
dell'interfaccia è per offrire maggiore libertà nell'implementazione

    _Possibili miglioramenti_: vedere se si può applicare in maniera più ragionata 
    il pattern Observer


### BenchmarkRun

Raccoglie insieme più TestRun, su cui poter calcolare Metrics aggregate.


### Cosa manca e possibili miglioramenti

- Potrebbe essere necessario riorganizzare i metodi presenti nelle classi 
  per rendere l'invocazione più logica (es. la classe Test ha il metodo run() 
  per eseguire un dato test e produrre una TestRun. Uno dei parametri del
  metodo potrebbe essere l'algoritmo).
 

