import pytest

from description.graph import Node, Edge


class TestEdge:

    @pytest.fixture
    def edge1(self):
        return Edge(Node(1), Node(2), 2)

    @pytest.fixture
    def edge2(self):
        return Edge(Node(5), Node(5))

    def test_start_node(self, edge1, edge2):
        assert edge1.start_node == Node(1)
        assert edge2.start_node == Node(5)

    def test_end_node(self, edge1, edge2):
        assert edge1.end_node == Node(2)
        assert edge2.end_node == Node(5)

    def test_weight(self, edge1, edge2):
        assert edge1.weight == 2
        assert edge2.weight == 1

    def test_equality(self, edge1, edge2):
        assert edge1 != Edge(Node(1), Node(2), weight=10)
        assert edge1 == Edge(Node(1), Node(2), weight=2)
        assert edge1 != edge2
        assert edge1 != "Ciao"

    def test_str(self, edge1):
        assert str(edge1) == "(1 [1, 0], 2 [0, 1] | 2)"
