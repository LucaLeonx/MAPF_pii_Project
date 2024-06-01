import globals
from description.entity_description import AgentDescription
from description.map.graph import Node
from result.action import MoveAction

test_run = globals.test_run()


class TestTestRun:

    def test_from_default_dict(self):
        # Just to be sure the current test instance works
        assert test_run.name == "Test1"
        assert len(test_run.action_list) == 11

    def test_getters(self):
        assert test_run.graph.nodes == [Node(1), Node(2), Node(3), Node(4)]
        assert AgentDescription("A1", "O1", Node(1)) in test_run.entities
        assert test_run.action_list[4].timestep == 1
        assert isinstance(test_run.action_list[5], MoveAction)


