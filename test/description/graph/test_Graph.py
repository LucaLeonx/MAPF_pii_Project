import pytest

from description.graph import *
from customexceptions import ElementNotFoundException


class TestGraph:
    @pytest.fixture
    def graph(self):
        return Graph([Edge(Node(1), Node(2)),
                      Edge(Node(1), Node(3)),
                      Edge(Node(2), Node(3)),
                      Edge(Node(3), Node(2), weight=7),
                      Edge(Node(3), Node(4), weight=-10)])

    def test_get_nodes(self, graph):
        assert graph.nodes == [Node(1), Node(2), Node(3), Node(4)]
        assert Node(1) in graph.nodes

    def test_has_node(self, graph):
        assert graph.has_node(Node(1))
        assert graph.has_node(Node(4))
        assert not graph.has_node(Node(5))

    def test_get_edges(self, graph):
        assert graph.edges == [Edge(Node(1), Node(2)),
                               Edge(Node(1), Node(3)),
                               Edge(Node(2), Node(3)),
                               Edge(Node(3), Node(2), weight=7),
                               Edge(Node(3), Node(4), weight=-10)]

    def test_get_adjacent_nodes(self, graph):
        assert graph.get_adjacent_nodes(Node(1)) == [Node(2), Node(3)]
        assert graph.get_adjacent_nodes(Node(2)) == [Node(3)]
        assert graph.get_adjacent_nodes(Node(4)) == []

        with pytest.raises(ElementNotFoundException) as excinfo:
            non_existent_node = graph.get_adjacent_nodes(Node(5))
        assert "Node 5 [0, 2] not found in graph" in str(excinfo.value)

    def test_get_edge(self, graph):
        assert graph.get_edge(Node(2), Node(3)) == Edge(Node(2), Node(3), weight=1)
        assert graph.get_edge(Node(3), Node(2)) == Edge(Node(3), Node(2), weight=7)

        with pytest.raises(ElementNotFoundException) as excinfo:
            non_existent_edge = graph.get_edge(Node(1), Node(1))
        assert "Edge (1 [1, 0], 1 [1, 0]) not found in graph" in str(excinfo.value)

    def test_str(self, graph):
        assert str(graph) == '''{
(1 [1, 0], 2 [0, 1] | 1)
(1 [1, 0], 3 [2, 0] | 1)
(2 [0, 1], 3 [2, 0] | 1)
(3 [2, 0], 2 [0, 1] | 7)
(3 [2, 0], 4 [1, 1] | -10)
}'''
