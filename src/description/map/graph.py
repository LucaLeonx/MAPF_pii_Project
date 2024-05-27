from math import floor, sqrt

from exceptions import EmptyElementException, InvalidElementException, ElementNotFoundException


class Graph:
    def __init__(self, edges):
        self._edges = list(set(edges)) # Remove duplicates
        self._node_adjacency_list = dict()

        for edge in edges:
            self._node_adjacency_list[edge.start_node] = []
            self._node_adjacency_list[edge.end_node] = []

        for edge in edges:
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
        return self._edges

    def has_edge(self, starting_node, ending_node):
        return Edge(starting_node, ending_node) in self._edges

    def get_edge(self, start_node, end_node):
        if self.has_edge(start_node, end_node):
            return self.edges[self.edges.index(Edge(start_node, end_node))]
        else:
            raise ElementNotFoundException(f"Edge ({start_node}, {end_node}) not found in graph")

    def __str__(self):
        return '{\n' + '\n'.join([str(edge) for edge in self._edges]) + '\n}'

    def to_dict(self, use_coords=False):
        return {"graph": [edge.to_dict(use_coords) for edge in self.edges]}

    @staticmethod
    def from_dict(dictionary):
        return Graph([Edge.from_dict(edge) for edge in dictionary["graph"]]) 

class UndirectedGraph(Graph):

    def __init__(self, edges):
        self._undirected_edges = []
        for edge in edges:
            self._undirected_edges.append(edge)
            self._undirected_edges.append(Edge(edge.ending_node, edge.starting_node, weight=edge.weight))

        super().__init__(self._undirected_edges)

    @property
    def undirected_edges(self):
        return self._undirected_edges

    def to_rdict(self, use_coords=False):
        return {"type": "undirected", "edges": [edge.to_dict(use_coords) for edge in self.edges]}


class GridGraph(UndirectedGraph):
    def __init__(self, rows, cols):

        if rows <= 0 or cols <= 0:
            raise InvalidElementException("Invalid negative number of rows or columns")

        self._rows = rows
        self._cols = cols

        edges = []

        for y in range(rows):
            for x in range(cols - 1):
                edges.append(Edge(Node(coords=(x, y)), Node(coords=(x + 1, y))))
                if y != rows - 1:
                    edges.append(Edge(Node(coords=(x, y)), Node(coords=(x, y + 1))))

        super().__init__(edges)

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    def to_rdict(self, use_coords=False):
        return {"type": "grid", "rows": self.rows, "cols": self.cols}

    @staticmethod
    def from_dict(dictionary):
        return GridGraph(dictionary["rows"], dictionary["cols"])

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
                self.end_node == other.end_node)

    def __hash__(self):
        return hash((self.start_node, self.end_node))

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
