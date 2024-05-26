import pytest

from benchmark.testdescription import TestDescription
from entity.agent_description import AgentDescription
from entity.objective_description import ObjectiveDescription
from entity.obstacle_description import ObstacleDescription
from graph.edge import Edge
from graph.graph import Graph
from graph.node import Node
from inspector.testinspector import TestInspector
from result.testrun import TestRun
from exceptions import OperationAlreadyDoneException, ElementNotAvailableException
from runner.testrecord import TestRecord


class TestTestRecord:

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
    def test_record(self, test_description):
        return TestRecord(test_description)

    def test_getters(self, test_record, test_description):
        assert not test_record.is_assigned()
        assert not test_record.is_done()
        assert test_record.get_test_name() == "Test1"
        assert test_record.get_test() == test_description

    def test_result_recording(self, test_record, test_description):
        test_record.assign_test()
        assert test_record.is_assigned()

        test_inspector = TestInspector(test_description)
        test_inspector.register_move(1, "T1", Node(2))
        test_inspector.register_move(2, "T1", Node(3))

        test_record.register_result(test_inspector.get_result())
        assert test_record.is_assigned()
        assert test_record.is_done()
        assert test_record.get_result()

    def test_operation_guards(self, test_record, test_description):

        test_record.assign_test()
        assert test_record.is_assigned()

        with pytest.raises(OperationAlreadyDoneException) as excinfo:
            test_record.assign_test()

        assert "Test already assigned" in str(excinfo.value)

        with pytest.raises(ElementNotAvailableException) as excinfo:
            test_record.get_result()

        assert "Test has not result yet" in str(excinfo.value)

        test_record.register_result(TestRun(test_description, [], True))

        with pytest.raises(OperationAlreadyDoneException) as excinfo:
            test_record.register_result(TestRun(test_description, [], False))

        assert "Test already done" in str(excinfo.value)




