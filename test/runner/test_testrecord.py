import pytest

from description.map.graph import Node
from inspector.testinspector import TestInspector
from result.testrun import TestRun
from exceptions import OperationAlreadyDoneException, ElementNotAvailableException
from runner.testrecord import TestRecord

import globals

test_description = globals.test_description()


class TestTestRecord:

    @pytest.fixture
    def test_record(self):
        return TestRecord(test_description)

    def test_getters(self, test_record):
        assert not test_record.is_assigned()
        assert not test_record.is_done()
        assert test_record.test_name == "Test1"
        assert test_record.test == test_description

    def test_result_recording(self, test_record):
        test_record.assign_test()
        assert test_record.is_assigned()

        test_inspector = TestInspector(test_description)
        test_inspector.register_move(1, "T1", Node(2))
        test_inspector.register_move(2, "T1", Node(3))

        test_record.register_result(test_inspector.get_result())
        assert test_record.is_assigned()
        assert test_record.is_done()
        assert test_record.get_result()

    def test_operation_guards(self, test_record):
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
