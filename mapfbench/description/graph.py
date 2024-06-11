"""
    Module for classes representing a Graph
"""

import importlib
from math import floor, sqrt
from typing import Any, Dict, Tuple, List

from utilities.customexceptions import EmptyElementException, InvalidElementException, ElementNotFoundException


class Graph:
    """
        Class for representing a directed, weighted graph.
        The instances of this class are immutable
    """

    def __init__(self, edges: List['Edge']):
        """
            Object initializer

            Parameters
            ----------
            edges : List[Edge]
                The list of edges comprising the graph
        """
        self._edges = list(set(edges))  # Remove duplicates
        self._node_adjacency_list = dict()

        for edge in edges:
            self._node_adjacency_list[edge.start_node] = []
            self._node_adjacency_list[edge.end_node] = []

        for edge in edges:
            self._node_adjacency_list[edge.start_node].append(edge.end_node)

    @property
    def nodes(self) -> List['Node']:
        """
            The nodes present in the Graph
        """
        return list(self._node_adjacency_list.keys())

    def has_node(self, node: 'Node') -> bool:
        """
            Check if a node is present in the graph

            Parameters
            ----------
            node : Node
                The Node to be checked for existence in the graph

            Returns
            -------
            bool
                True if the node is present in the graph, False otherwise
        """
        return node in self._node_adjacency_list.keys()

    def get_adjacent_nodes(self, node: 'Node') -> List['Node']:
        """
            Returns the list of nodes adjacent to the supplied one
            (can be reached with an edge starting from the node),
            provided that it is present in the graph.

            Parameters
            ----------
            node : Node
                The node whose neighbours are sought

            Returns
            -------
            list[Node]
                A list of the adjacent nodes

            Raises
            ------
            ElementNotFoundException
                If the node is not in the graph
        """
        if self.has_node(node):
            return self._node_adjacency_list[node]
        else:
            raise ElementNotFoundException(f"Node {node} not found in graph")

    @property
    def edges(self) -> List['Edge']:
        """
            The edges present in the graph
        """
        return self._edges

    def has_edge(self, start_node: 'Node', end_node: 'Node') -> bool:
        """
            Check if an edge with the specified start and end node is present in the graph

            Parameters
            ----------
            start_node : Node
                The starting node of the edge to check for existence

            end_node: Node
                The ending node of the edge to check for existence

            Returns
            -------
            bool
                True if the edge is present in the graph, False otherwise
        """
        return Edge(start_node, end_node) in self._edges

    def get_edge(self, start_node: 'Node', end_node: 'Node') -> 'Edge':
        """
            Returns the edge of the graph with the specified start and end node.
            The edge must be present in the graph.

            This method is useful to retrieve the weight of a specific edge of the graph

            Parameters
            ----------
            start_node : Node
                    The starting node of the requested edge

            end_node: Node
                    The ending node of the requested edge

            Returns
            -------
            Edge
                The corresponding edge in the graph, with the specified start and end nodes

            Raises
            ------
            ElementNotFoundException
                If the requested edge is not present in the graph
        """
        if self.has_edge(start_node, end_node):
            return self.edges[self.edges.index(Edge(start_node, end_node))]
        else:
            raise ElementNotFoundException(f"Edge ({start_node}, {end_node}) not found in graph")

    def __str__(self):
        return '{\n' + '\n'.join([str(edge) for edge in self._edges]) + '\n}'

    def to_dict(self):
        return {"type": self.__class__.__name__, "edges": [edge.to_dict() for edge in self.edges]}

    @classmethod
    def _from_dict(cls, dictionary):
        return Graph([Edge.from_dict(edge) for edge in dictionary["edges"]])

    @staticmethod
    def from_dict(dictionary):
        module = importlib.import_module(__name__)
        graph_class = getattr(module, dictionary["type"])

        return graph_class._from_dict(dictionary)


class UndirectedGraph(Graph):
    """
        A class representing an undirected, weighted graph.
        For each edge, the reversed one is present
    """
    def __init__(self, edges: List['Edge']):
        """
            Object initializer

            Parameters
            ----------
            edges : List[Edge]
                The list of edges comprising the graph. They are assumed to be undirected
        """
        self._undirected_edges = []
        self._edges = []
        for edge in edges:
            if edge.reversed() not in self._edges:
                self._undirected_edges.append(edge)
                self._edges.append(edge)
                self._edges.append(edge.reversed())

        super().__init__(self._edges)

    @property
    def undirected_edges(self) -> List['Edge']:
        """
            The list of undirected edges of the graph
        """
        return self._undirected_edges

    @classmethod
    def _from_dict(cls, dictionary):
        return UndirectedGraph(dictionary["edges"])


class GridGraph(UndirectedGraph):
    """
        A GridGraph is a special type of `Graph` used to represent a grid.
        It has the following properties:
        - It is an `UndirectedGraph`
        - Each edge has weight 1
        - Nodes and edges are arranged to form a grid
    """
    def __init__(self, rows: int, cols: int):
        """
            Object initializer

            Parameters
            ----------
            rows: int
                The number of rows of the grid
            cols: int
                The number of columns of the grid

            Raises
            ------
            InvalidElementException
                If either the number of `rows` or `cols` specified is zero or negative
        """
        if rows <= 0 or cols <= 0:
            raise InvalidElementException("Invalid negative or null number of rows or columns")

        self._rows = rows
        self._cols = cols

        edges = []

        for y in range(rows):
            for x in range(cols):
                # length of rows = number of cols
                # length of cols = number of rows
                if x + 1 < cols:
                    edges.append(Edge(Node(coords=(x, y)), Node(coords=(x + 1, y))))
                if x - 1 >= 0:
                    edges.append(Edge(Node(coords=(x, y)), Node(coords=(x - 1, y))))
                if y + 1 < rows:
                    edges.append(Edge(Node(coords=(x, y)), Node(coords=(x, y + 1))))
                if y - 1 >= 0:
                    edges.append(Edge(Node(coords=(x, y)), Node(coords=(x, y - 1))))

        super().__init__(edges)

    @property
    def rows(self) -> int:
        """
            The number of rows in the grid
        """
        return self._rows

    @property
    def cols(self) -> int:
        """
            The number of columns in the grid
        """
        return self._cols

    @property
    def dimensions(self) -> Tuple[int, int]:
        """
            The dimensions (rows x cols) of the grid
        """
        return self.rows, self.cols

    def to_dict(self):
        return {"type": self.__class__.__name__, "rows": self.rows, "cols": self.cols}

    @classmethod
    def _from_dict(cls, dictionary):
        return GridGraph(dictionary["rows"], dictionary["cols"])


class Edge:
    """
        A directed, weighted edge in a graph

        An edge is identified by its start and end node.
        Moreover, edges have a weight as well.
        Two edges are considered equal if and only if
        they have the same start and end node (weight is
        not taken into account).

        The instances of this class are immutable
    """

    def __init__(self, start_node: 'Node', end_node: 'Node', weight: float = 1):
        """
            Object initializer

            Parameters
            ----------
            start_node : Node
                The starting node of the edge
            end_node: Node
                The ending node of the edge
            weight: float, optional
                The weight of the edge

        """
        self._start_node = start_node
        self._end_node = end_node
        self._weight = weight

    @property
    def start_node(self) -> 'Node':
        """
            The starting node of the edge
        """
        return self._start_node

    @property
    def end_node(self) -> 'Node':
        """
            The ending node of the edge
        """
        return self._end_node

    @property
    def weight(self) -> float:
        """
            The weight of the edge
        """
        return self._weight

    def reversed(self) -> 'Edge':
        """
            Returns
            -------
            Edge
                A new Edge, whose start and end nodes are those of the initial one, reversed.
                The weight of the new Edge is equal to that of the initial one
        """
        return Edge(self.end_node, self.start_node, self.weight)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.start_node == other.start_node and
                self.end_node == other.end_node)

    def __hash__(self):
        return hash((self.start_node, self.end_node))

    def __str__(self):
        return f"({self.start_node}, {self.end_node} | {self.weight})"

    def to_dict(self) -> Dict[str, Any]:
        return {"start_node": self.start_node.to_dict(),
                "end_node": self._end_node.to_dict(),
                "weight": self._weight}

    @staticmethod
    def from_dict(dictionary):
        return Edge(Node.from_dict(dictionary["start_node"]),
                    Node.from_dict(dictionary["end_node"]),
                    dictionary["weight"])


class Node:
    """
        A Node in a graph.

        A Node may be either identified by a non-negative index or
        by its non-negative coordinates. The class establishes a
        bijection between the index and the corresponding coordinates
        of a node. Two nodes are considered equal if and only if
        they have the same corresponding index.

        The instances of this class are immutable.
    """

    @classmethod
    def _cantor_pairing_function(cls, numbers: Tuple[int, int]) -> int:
        a, b = numbers
        return (a + b) * (a + b + 1) // 2 + b

    @classmethod
    def _cantor_inverse_pairing_function(cls, n: int) -> Tuple[int, int]:
        w = floor((sqrt(8 * n + 1) - 1) / 2)
        t = (w ** 2 + w) / 2
        return int(w - n + t), int(n - t)

    def __init__(self, index: int = None, coords: Tuple[int, int] = None):
        """
            Object initializer

            At least one of the optional parameters `index` or `coords` must be specified.
            If both are supplied, `index` takes precedence.

            Parameters
            ----------
            index : int
                The index of the node in the graph.
                It must be non-negative
            coords : Tuple[int, int]
                The cartesian coordinates (x, y) of the node in the graph.
                They must be both non-negative

            Raises
            ------
            EmptyElementException
                If neither `index` nor `coords` were specified
            InvalidElementException
                If negative values where used for `index` or `coords`
        """

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
    def index(self) -> int:
        """
            The index of the node
        """
        return self._index

    @property
    def coords(self) -> Tuple[int, int]:
        """
            The coordinates of the node
        """
        return self._x, self._y

    @property
    def x(self) -> int:
        """
            The x coordinate of the node
        """
        return self._x

    @property
    def y(self) -> int:
        """
            The y coordinate of the node
        """
        return self._y

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.index == other.index)

    def __hash__(self):
        return hash(self._index)

    def __str__(self):
        return f"{self.index} [{self.x}, {self.y}]"

    def to_dict(self, use_coords: bool = False) -> Dict[str, Any]:
        """
            Returns a dictionary representation of the node.

            Parameters
            ----------
            use_coords : bool
                If False, the node will be represented with its index.
                e.g {"index": 1}
                If True, the coordinates will be used instead
                {"x": 2, "y": 3}

            Returns
            -------
            Dict[str, Any]
                A dictionary with the information associated to the node
        """
        if not use_coords:
            return {"index": self._index}
        else:
            return {"x": self.x, "y": self.y}

    @staticmethod
    def from_dict(dictionary: Dict[str, Any]) -> 'Node':
        """
            Returns a `Node` instance from a dictionary.


            Parameters
            ----------
            dictionary :
                The dictionary to convert. The format must be one of
                those generated by the `to_dict()` function


            Returns
            -------
            Node
                The node corresponding to the given dictionary
        """
        if "index" in dictionary:
            return Node(index=dictionary["index"])
        else:
            return Node(coords=(dictionary["x"], dictionary["y"]))
