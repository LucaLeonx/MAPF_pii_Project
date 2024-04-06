import pytest
from _pytest import unittest
from graph.Node import Node


class TestNode:

    @pytest.fixture(autouse=True)
    def node1(self):
        return Node(index=1, adjacent_nodes_index=[1, 2])

    @pytest.fixture(autouse=True)
    def node2(self):
        return Node(index=2)

    @pytest.fixture(autouse=True)
    def node3(self):
        return Node(coordinates=(1, 1), adjacent_nodes_index=[2])

    def test_cantor_functions(self):
        assert Node._cantor_pairing_function((1, 1)) == 4
        assert Node._cantor_inverse_pairing_function(4) == (1, 1)
        assert Node._cantor_pairing_function(Node._cantor_inverse_pairing_function(150)) == 150

    def test_init_guards(self):
        with pytest.raises(ValueError) as excinfo:
            node = Node()
        assert "A Node must be identified by either its index or its coordinates" in str(excinfo.value)

        with pytest.raises(ValueError) as excinfo:
            node = Node(index=-1)
        assert "The node index cannot be negative" in str(excinfo.value)

        with pytest.raises(ValueError) as excinfo:
            node = Node(coordinates=(-1, 10))
        assert "The node coordinates cannot be negative" in str(excinfo.value)

    def test_get_index(self, node1, node2, node3):
        assert node1.get_index() == 1
        assert node2.get_index() == 2
        assert node3.get_index() == 4

    def test_get_coordinates(self, node1, node2, node3):
        assert node1.get_coordinates() == (1, 0)
        assert node2.get_coordinates() == (0, 1)
        assert node3.get_coordinates() == (1, 1)

    def test_get_adjacent_nodes(self, node1, node2, node3):
        assert node1.get_adjacent_nodes_index() == [1, 2]
        assert node2.get_adjacent_nodes_index() == []
        assert node3.get_adjacent_nodes_index() == [2]

    def test_string_representation(self, node1):
        assert str(node1) == "Node[1] (1, 0)"

    def test_equality(self):
        assert Node(1) == Node(coordinates=(1, 0))
        assert Node(2) == Node(coordinates=(0, 1))
        assert Node(0) == Node(coordinates=(0, 0))
        assert Node(1) != Node(coordinates=(0, 0))
        assert Node(1) != "Ciao"
