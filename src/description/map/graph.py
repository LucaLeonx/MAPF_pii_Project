from math import floor, sqrt

from exceptions import EmptyElementException, InvalidElementException, ElementNotFoundException


class Graph:
    def __init__(self, edge_list):
        self._edge_list = edge_list
        self._node_adjacency_list = dict()

        for edge in edge_list:
            self._node_adjacency_list[edge.start_node] = []
            self._node_adjacency_list[edge.end_node] = []

        for edge in edge_list:
            self._node_adjacency_list[edge.start_node].append(edge.end_node)

    @property
    def nodes(self):
        return list(self._node_adjacency_list.keys())

    def has_node(self, node):
        return node in self._node_adjacency_list.keys()

    def get_adjacent_nodes(self, node):
        if self.has_node(node):
            return self._node_adjacency_list[node]
        else:
            raise ElementNotFoundException(f"Node {node} not found in graph")

    @property
    def edges(self):
        return self._edge_list

    def has_edge(self, starting_node, ending_node):
        try:
            self.get_edge(starting_node, ending_node)
        except ElementNotFoundException:
            return False

        return True

    def get_edge(self, start_node, end_node):
        edge = [edge for edge in self.edges if edge.start_node == start_node and
                edge.end_node == end_node]
        if edge:
            return edge[0]
        else:
            raise ElementNotFoundException(f"Edge ({start_node}, {end_node}) not found in graph")

    def __str__(self):
        return '{\n' + '\n'.join([str(edge) for edge in self._edge_list]) + '\n}'

    def to_dict(self):
        return {"graph": [edge.to_dict() for edge in self.edges]}

    @staticmethod
    def from_dict(dictionary):
        return Graph([Edge.from_dict(edge) for edge in dictionary["graph"]])


class Edge:
    def __init__(self, start_node, end_node, weight=1):
        self._start_node = start_node
        self._end_node = end_node
        self._weight = weight

    @property
    def start_node(self):
        return self._start_node

    @property
    def end_node(self):
        return self._end_node

    @property
    def weight(self):
        return self._weight

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.start_node == other.start_node and
                self.end_node == other.end_node and
                self.weight == other.weight)

    def __hash__(self):
        return hash((self.start_node, self.end_node, self._weight))

    def __str__(self):
        return f"({self.start_node}, {self.end_node} | {self.weight})"

    def to_dict(self, use_coords=False):
        return {"start_node": self.start_node.to_dict(use_coords),
                "end_node": self._end_node.to_dict(use_coords),
                "weight": self._weight}

    @staticmethod
    def from_dict(dictionary):
        return Edge(Node.from_dict(dictionary["start_node"]),
                    Node.from_dict(dictionary["end_node"]),
                    dictionary["weight"])


class Node:

    @classmethod
    def _cantor_pairing_function(cls, numbers):
        a, b = numbers
        return (a + b) * (a + b + 1) // 2 + b

    @classmethod
    def _cantor_inverse_pairing_function(cls, n):
        w = floor((sqrt(8 * n + 1) - 1) / 2)
        t = (w ** 2 + w) / 2
        return int(w - n + t), int(n - t)

    def __init__(self, index=None, coords=None):
        if index is None and coords is None:
            raise EmptyElementException("A Node must be identified by either its index or its coordinates")
        elif index is not None:
            if index < 0:
                raise InvalidElementException("The node index cannot be negative")
            else:
                self._index = index
                self._x, self._y = self._cantor_inverse_pairing_function(index)
        else:
            if coords[0] < 0 or coords[1] < 0:
                raise InvalidElementException("The node coordinates cannot be negative")
            else:
                self._index = self._cantor_pairing_function(coords)
                self._x, self._y = coords

    @property
    def index(self):
        return self._index

    @property
    def coords(self):
        return self._x, self._y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.index == other.index)

    def __hash__(self):
        return hash(self._index)

    def __str__(self):
        return f"{self.index} [{self.x}, {self.y}]"

    def to_dict(self, use_coords=False):
        if not use_coords:
            return {"index": self._index}
        else:
            return {"x": self.x, "y": self.y}

    @staticmethod
    def from_dict(dictionary):
        if "index" in dictionary:
            return Node(index=dictionary["index"])
        else:
            return Node(coords=(dictionary["x"], dictionary["y"]))
