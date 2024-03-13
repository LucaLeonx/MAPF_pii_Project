import igraph as ig

class DirectedGraph():
   
    def __init__(self, edge_list):
        self._graph = ig.Graph(edges=edge_list, directed=True)

    def is_node_present(self, position):
        # Using this expression ensures a boolean is returned
        if self._graph.vs.select(position):
            return True
        else:
            return False

    def is_edge_present(self, start_node, end_node):
        if self._graph.es.select(_from=start_node, _to=end_node):
            return True
        else:
            return False

    
    #def get_adjacent_nodes(self, node): 
    #   return self._graph.successors(node)

