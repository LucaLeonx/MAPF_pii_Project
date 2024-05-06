import ntpath

from optional import Optional
from graph.node import Node
from graph.edge import Edge


class Graph:
    def __init__(self, edge_list):
        self._edge_list = edge_list
        self._node_adjacency_list = dict()

        for edge in edge_list:
            self._node_adjacency_list[edge.get_start_node()] = []
            self._node_adjacency_list[edge.get_end_node()] = []

        for edge in edge_list:
            self._node_adjacency_list[edge.get_start_node()] += [edge.get_end_node()]

    def get_nodes(self):
        return list(self._node_adjacency_list.keys())

    def has_node(self, node):
        return node in self._node_adjacency_list.keys()

    def get_adjacent_nodes(self, node):
        if self.has_node(node):
            return self._node_adjacency_list[node]
        else:
            raise ValueError(f"Node {node} not found in graph")

    def get_edges(self):
        return self._edge_list

    def has_edge(self, starting_node, ending_node):
        try:
            self.get_edge(starting_node, ending_node)
        except ValueError:
            return False

        return True

    def get_edge(self, start_node, end_node):
        edge = [edge for edge in self._edge_list if edge.get_start_node() == start_node and
                edge.get_end_node() == end_node]
        if edge:
            return edge[0]
        else:
            raise ValueError(f"Edge ({start_node}, {end_node}) not found in graph")

    def __str__(self):
        return '{\n' + '\n'.join([str(edge) for edge in self._edge_list]) + '\n}'

    def to_dict(self, use_coordinates=False):
        return {"graph": [edge.to_dict(use_coordinates) for edge in self._edge_list]}

    @staticmethod
    def from_dict(dictionary, use_coordinates=False):
        return Graph([Edge.from_dict(edge, use_coordinates) for edge in dictionary["graph"]])

