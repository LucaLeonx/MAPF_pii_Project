import pytest

from description.benchmarkdescription import TestDescription

import globals
from customexceptions import OperationAlreadyDoneException
from result.testrun import TestRun
from runner.testmanager import TestManager

default_test = globals.test_description()


def _generate_test_instance(name, old_test) -> TestDescription:
    return TestDescription(name, old_test.graph, old_test.entities)


class TestTestManager:

    @pytest.fixture(autouse=True)
    def test_instances(self):
        return {_generate_test_instance("Test1", default_test): 1,
                _generate_test_instance("Test2", default_test): 2,
                _generate_test_instance("Test3", default_test): 3}

    @pytest.fixture(autouse=True)
    def test_runs(self, test_instances):
        return dict([(item[0].name, TestRun(item[0], [], True)) for item in test_instances.items()])

    @pytest.fixture(autouse=True)
    def test_manager(self, test_instances):
        return TestManager(test_instances)

    def test_start(self, test_manager):
        assert [record.test_name for record in test_manager.get_test_records()] == ["Test1", "Test2", "Test3"]
        assert [record.remaining_occurrences for record in test_manager.get_test_records()] == [1, 2, 3]
        assert not test_manager.all_tests_done()

    # TODO: Problem: if 3 instances of a test are needed, but 3 are assigned,
    # the random tester won't assign any test. However, if results don't arrive,
    # the runner may wait indefinitely. Solution, ask the users to rerun the missed tests.

    def test_getters_of_description(self, test_manager):
        record = test_manager.get_test_record_by_name("Test3")
        assert record.test_name == "Test3"
        assert record.remaining_occurrences == 3

    def test_results_recording(self, test_manager, test_runs):
        test_manager.record_test_result(test_runs["Test1"])
        test_manager.record_test_result(test_runs["Test2"])
        test_manager.record_test_result(test_runs["Test3"])

        assert [record.remaining_occurrences for record in test_manager.get_test_records()] == [0, 1, 2]
        assert not test_manager.all_tests_done()

    def test_record_all_results(self, test_manager, test_runs):
        test_manager.record_test_result(test_runs["Test1"])
        test_manager.record_test_result(test_runs["Test2"])
        test_manager.record_test_result(test_runs["Test3"])
        test_manager.record_test_result(test_runs["Test2"])
        test_manager.record_test_result(test_runs["Test3"])
        test_manager.record_test_result(test_runs["Test3"])

        assert [record.remaining_occurrences for record in test_manager.get_test_records()] == [0, 0, 0]
        assert test_manager.all_tests_done()

    def test_excessive_submissions(self, test_manager, test_runs):

        test_manager.record_test_result(test_runs["Test2"])
        test_manager.record_test_result(test_runs["Test2"])

        with pytest.raises(OperationAlreadyDoneException) as excinfo:
            test_manager.record_test_result(test_runs["Test2"])
        assert "Test already done" in str(excinfo.value)


