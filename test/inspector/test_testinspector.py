import pytest

from benchmark.testdescription import TestDescription
from entity.agent_description import AgentDescription
from entity.objective_description import ObjectiveDescription
from entity.obstacle_description import ObstacleDescription
from graph.edge import Edge
from graph.graph import Graph
from graph.node import Node
from inspector.testinspector import TestInspector


class TestTestInspector:

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
                                Edge(Node(3), Node(4))
                                ])

    @pytest.fixture
    def test_description(self, graph, entity_list):
        return TestDescription("Test1", graph, entity_list)

    @pytest.fixture
    def test_inspector(self, test_description):
        return TestInspector(test_description)

    def test_mark_as_solved(self, test_inspector):
        result = test_inspector.get_result()
        assert not result.is_solved

        test_inspector.mark_as_solved()
        result = test_inspector.get_result()
        assert result.is_solved

    def test_default_entity_appearance(self, test_inspector, test_description):
        result = test_inspector.get_result()

        assert result.test_description == test_description
        assert len(result.action_list) == len(test_description.get_agents())

        for entity in test_description.get_agents():
            appearance = [action for action in result.action_list if action.subject == entity.get_name()]
            assert len(appearance) == 1
            assert appearance[0].timestep == 0
            assert appearance[0].position == entity.get_start_position()

        not_appeared_names = [entity.get_name() for entity in test_description.get_obstacles() + test_description.get_objectives()]
        assert not [action for action in result.action_list if action.subject in not_appeared_names]

    def test_action_recording(self, test_inspector):
        test_inspector.register_move(1, "A1", Node(1))  # 3
        test_inspector.register_move(1, "A2", Node(3))  # 4
        test_inspector.register_move(1, "A3", Node(4))  # 5
        test_inspector.register_wait(2, "A2")  # 6
        test_inspector.register_disappearance(2, "A1")  # 7
        test_inspector.register_appearance(3, "T3", Node(coordinates=(2, 2)))  # 8
        test_inspector.register_move_left(4, "T3")  # 9
        test_inspector.register_move_up(5, "T3")  # 10

        action_list = test_inspector.get_result().action_list

        assert len(action_list) == 11  # plus agents appearances (3 actions)
        assert action_list[4].subject == "A2"
        assert action_list[4].description == "Move"
        assert action_list[4].position == Node(3)
        assert action_list[4].__class__.__name__ == "MoveAction"
        assert action_list[6].description == "Wait"
        assert action_list[9].position == Node(coordinates=(1, 2))
        assert action_list[9].description == "MoveLeft"
        assert action_list[10].position == Node(coordinates=(1, 3))
        assert action_list[10].description == "MoveUp"





