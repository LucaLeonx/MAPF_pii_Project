import pytest
from graph.edge import Edge
from graph.node import Node


class TestEdge:

    @pytest.fixture
    def edge1(self):
        return Edge(Node(1), Node(2), 2)

    @pytest.fixture
    def edge2(self):
        return Edge(Node(5), Node(5))

    def test_get_start_node(self, edge1, edge2):
        assert edge1.get_start_node() == Node(1)
        assert edge2.get_start_node() == Node(5)

    def test_get_end_node(self, edge1, edge2):
        assert edge1.get_end_node() == Node(2)
        assert edge2.get_end_node() == Node(5)

    def test_get_weight(self, edge1, edge2):
        assert edge1.get_weight() == 2
        assert edge2.get_weight() == 1

    def test_equality(self, edge1, edge2):
        assert edge1 == Edge(Node(1), Node(2), weight=10)
        assert edge1 != edge2
        assert edge1 != "Ciao"