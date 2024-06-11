import pytest

from description.map.graph import Node
from inspector.testinspector import TestInspector

import globals

test_description = globals.test_description()


class TestTestInspector:

    @pytest.fixture
    def test_inspector(self):
        return TestInspector(test_description)

    def test_mark_as_solved(self, test_inspector):
        result = test_inspector.get_result()
        assert not result.is_solved

        test_inspector.mark_as_solved()
        result = test_inspector.get_result()
        assert result.is_solved

    def test_default_entity_appearance(self, test_inspector):
        result = test_inspector.get_result()

        assert result.test_description == test_description
        assert len(result.action_list) == len(test_description.agents)

        for entity in test_description.agents:
            appearance = [action for action in result.action_list if action.subject == entity.name]
            assert len(appearance) == 1
            assert appearance[0].timestep == 0
            assert appearance[0].end_position == entity.start_position

        not_appeared_names = [entity.name for entity in
                              test_description.obstacles + test_description.objectives]
        assert not [action for action in result.action_list if action.subject in not_appeared_names]

    def test_action_recording(self, test_inspector):
        test_inspector.start_profiling()
        test_inspector.end_profiling()
        test_inspector.register_move(1, "A1", Node(1))  # 3
        test_inspector.register_move(1, "A2", Node(3))  # 4
        test_inspector.register_move(1, "A3", Node(4))  # 5
        test_inspector.register_wait(2, "A2")  # 6
        test_inspector.register_disappearance(2, "A1")  # 7
        test_inspector.register_appearance(3, "T3", Node(coords=(2, 2)))  # 8
        test_inspector.register_move_left(4, "T3")  # 9
        test_inspector.register_move_up(5, "T3")  # 10

        action_list = test_inspector.get_result().action_list
        print(test_inspector.get_result().to_dict())

        assert len(action_list) == 11  # plus agents appearances (3 actions)
        assert action_list[4].subject == "A2"
        assert action_list[4].description == "Move"
        assert action_list[4].end_position == Node(3)
        assert action_list[4].__class__.__name__ == "MoveAction"
        assert action_list[6].description == ""
        assert action_list[9].end_position == Node(coords=(1, 2))
        assert action_list[9].description == "MoveLeft"
        assert action_list[10].end_position == Node(coords=(1, 3))
        assert action_list[10].description == "MoveUp"
