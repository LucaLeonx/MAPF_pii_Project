import pytest

from graph.node import Node
from graph.edge import Edge
from graph.graph import Graph


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
        assert graph.get_node(1) == Node(1)
        assert graph.get_node(1).get_adjacent_nodes_index() == [2, 3]

        with pytest.raises(ValueError) as excinfo:
            non_existent_node = graph.get_node(5)
        assert "Node with index (5) not found in graph" in str(excinfo.value)

    def test_get_edge(self, graph):
        assert graph.get_edge(2, 3) == Edge(Node(2), Node(3))

        with pytest.raises(ValueError) as excinfo:
            non_existent_edge = graph.get_edge(1, 1)
        assert "Edge (1, 1) not found in graph" in str(excinfo.value)
