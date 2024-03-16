from graph.directedgraph import DirectedGraph
from entity import Entity

class Test():
    
    def __init__ (self, field, entities):
        self._field = field
        self._entities = entities
    
    def get_field(self):
        return self._field

    def get_entities(self):
        return self._entities

