import pytest

from description.benchmarkdescription import TestDescription
from description.entity_description import *
from description.map.graph import *


class TestTestDescription:

    @pytest.fixture
    def entity_list(self):
        objective1 = ObjectiveDescription("T1")
        objective2 = ObjectiveDescription("T2")
        objective3 = ObjectiveDescription("T3")

        agent1 = AgentDescription("A1", "T1", start_position=Node(1))
        agent2 = AgentDescription("A2", "T2", start_position=Node(2))
        agent3 = AgentDescription("A3", "T3", start_position=Node(3))

        obstacle = ObstacleDescription("O1")

        return [objective1, objective2, objective3, agent1, agent2, agent3, obstacle]

    @pytest.fixture
    def graph(self):
        return Graph(edge_list=[Edge(Node(1), Node(2)),
                                Edge(Node(1), Node(3)),
                                Edge(Node(2), Node(3)),
                                Edge(Node(3), Node(2)),
                                Edge(Node(3), Node(4))])

    @pytest.fixture
    def test_description(self, graph, entity_list):
        return TestDescription("Test1", graph, entity_list)

    def test_init_guard(self, graph, entity_list):
        with pytest.raises(EmptyElementException) as excinfo:
            test = TestDescription("", graph, entity_list)
        assert "Test name cannot be empty" in str(excinfo.value)

        with pytest.raises(EmptyElementException) as excinfo:
            test = TestDescription("        ", graph, entity_list)
        assert "Test name cannot be empty" in str(excinfo.value)

    def test_get_name(self, test_description):
        assert test_description.name == "Test1"

    def test_get_map(self, test_description, graph):
        assert test_description.graph == graph

    def test_get_entities(self, test_description, entity_list):
        assert test_description.entities == entity_list

    def test_get_agents(self, test_description, entity_list):
        assert test_description.agents == entity_list[3:6]

    def test_get_obstacles(self, test_description, entity_list):
        assert test_description.obstacles == [entity_list[-1]]

    def test_get_objectives(self, test_description, entity_list):
        assert test_description.objectives == entity_list[:3]

    def test_empty_test(self):
        test = TestDescription("Empty", Graph(edge_list=[]), [])
        assert test.agents == []