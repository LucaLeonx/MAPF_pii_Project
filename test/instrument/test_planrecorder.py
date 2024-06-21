import numpy as np
import pytest

from mapfbench.description import Action, ActionType
from mapfbench.instrument.planrecorder import PlanRecorder

p = np.array
eq = np.array_equal


class TestPlanRecorder:

    def test_initialization(self, generic_scenario):
        recorder = PlanRecorder(generic_scenario)
        assert np.array_equal(recorder.actions, p([]))
        assert not recorder.is_solved
        assert recorder.scenario.map.width == generic_scenario.map.width

    def test_action_recording(self, generic_scenario):
        recorder = PlanRecorder(generic_scenario)
        recorder.record(Action(1, 1, ActionType.MOVE, end_position=p([2, 0])))
        recorder.record_move(2, 1, p([1, 1]))
        recorder.record_move(3, 1, p([2, 1]))
        recorder.record_wait(10, 2)

        assert np.size(recorder.actions) == 4

        print([str(action) + '\n' for action in recorder.actions])
        assert [str(action) for action in recorder.actions] == [
            't: 1 Agent ID: 1, action: MOVE start:None end:[2 0]',
            't: 2 Agent ID: 1, action: MOVE start:[2 0] end:[1 1]',
            't: 3 Agent ID: 1, action: MOVE start:[1 1] end:[2 1]',
            't: 10 Agent ID: 2, action: WAIT start:[0 2] end:[0 2]']

        recorder.mark_as_solved()
        assert recorder.is_solved


