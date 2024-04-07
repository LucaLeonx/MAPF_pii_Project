from optional import Optional
from graph.node import Node
from graph.edge import Edge


class Graph:
    def __init__(self, edge_list):
        self._edge_list = edge_list
        _node_adjacency_list = dict()
        self._node_list = []

        for edge in edge_list:
            _node_adjacency_list[edge.get_start_node().get_index()] = []
            _node_adjacency_list[edge.get_end_node().get_index()] = []

        for edge in edge_list:
            _node_adjacency_list[edge.get_start_node().get_index()] += [edge.get_end_node().get_index()]

        for (node, adjacent_nodes) in _node_adjacency_list.items():
            self._node_list.append(Node(index=node, adjacent_nodes_index=adjacent_nodes))

    def get_nodes(self):
        return self._node_list

    def get_edges(self):
        return self._edge_list

    def get_node(self, index):
        node = [node for node in self._node_list if node.get_index() == index]
        if node:
            return node[0]
        else:
            raise ValueError(f"Node with index ({index}) not found in graph")

    def get_edge(self, start_node, end_node):
        edge = [edge for edge in self._edge_list if edge.get_start_node() == Node(start_node) and
                edge.get_end_node() == Node(end_node)]
        if edge:
            return edge[0]
        else:
            raise ValueError(f"Edge ({start_node}, {end_node}) not found in graph")
