import pytest

from graph.Node import Node
from graph.Edge import Edge
from graph.Graph import Graph


class TestGraph:
    @pytest.fixture
    def graph(self):
        return Graph(edge_list=[Edge(Node(1), Node(2)),
                                Edge(Node(1), Node(3)),
                                Edge(Node(2), Node(3)),
                                Edge(Node(3), Node(2)),
                                Edge(Node(3), Node(4))
                                ])

    def test_get_nodes(self, graph):
        assert graph.get_nodes() == [Node(1), Node(2), Node(3), Node(4)]

    def test_get_edges(self, graph):
        assert graph.get_edges() == [Edge(Node(1), Node(2)),
                                     Edge(Node(1), Node(3)),
                                     Edge(Node(2), Node(3)),
                                     Edge(Node(3), Node(2)),
                                     Edge(Node(3), Node(4))
                                     ]

    def test_get_node(self, graph):
        assert graph.get_node(1).get() == Node(1)
        assert graph.get_node(1).get().get_adjacent_nodes_index() == [2, 3]
        assert graph.get_node(5).is_empty()

    def test_get_edge(self, graph):
        assert graph.get_edge(2, 3).get() == Edge(Node(2), Node(3))
        assert graph.get_edge(1, 1).is_empty()
