import igraph as ig

class DirectedGraph():
   
    def __init__(self, edge_list):
        self._graph = ig.Graph(edges=edge_list, directed=True)

    def is_node_present(self, position):
        # Using this expression ensures a boolean is returned
        return position >= 0 and position < self._graph.vcount()

    def is_edge_present(self, start_node, end_node):
        return self.is_node_present(start_node) and self.is_node_present(end_node) and self._graph.are_connected(start_node, end_node)           
    def get_adjacent_nodes(self, node):
        if self.is_node_present(node):
            return self._graph.successors(node)
        else:
            return []

