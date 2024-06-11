import pytest

from description.graph import UndirectedGraph, Edge, Node


class TestUndirectedGraph:

    @pytest.fixture(autouse=True)
    def undirected_graph(self):
        return UndirectedGraph([Edge(Node(1), Node(2)),
                                Edge(Node(2), Node(3)),
                                Edge(Node(3), Node(1))
                                ])

    def test_edges(self, undirected_graph):
        for edge in undirected_graph.edges:
            assert undirected_graph.has_edge(edge.end_node, edge.start_node)

        assert set(undirected_graph.undirected_edges) == {Edge(Node(1), Node(2)),
                                                          Edge(Node(2), Node(3)),
                                                          Edge(Node(3), Node(1))}

        assert len(undirected_graph.edges) == len(undirected_graph.undirected_edges) * 2
