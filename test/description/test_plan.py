import pytest
import numpy as np

from mapfbench.description.plan import Action, ActionType, Plan
from mapfbench.description.scenario import Agent


class TestAction:

    def test_getters(self):
        action = Action(timestep=0,
                        subject_id=1,
                        action_type=ActionType.MOVE,
                        start_position=[0, 1],
                        end_position=[1, 0])
        assert action.subject_id == 1
        assert np.array_equal(action.start_position, np.array([0, 1]))
        assert np.array_equal(action.end_position, np.array([1, 0]))
        assert action.action_type == ActionType.MOVE

    def test_init_guards(self):
        with pytest.raises(ValueError) as e:
            action = Action(timestep=-1, subject_id=1, action_type=ActionType.MOVE)
        assert str(e.value) == "Cannot use negative timestep in Action"

    def test_str(self):
        assert str(Action(1, 2, ActionType.MOVE)) == 't: 1 Agent ID: 2, action: MOVE start:None end:None'
        assert str(Action(1, 2, ActionType.MOVE,
                          start_position=[1, 0])) == 't: 1 Agent ID: 2, action: MOVE start:[1 0] end:None'
        assert str(Action(1, 2, ActionType.MOVE,
                          end_position=[0, 1])) == 't: 1 Agent ID: 2, action: MOVE start:None end:[0 1]'
        assert str(Action(1, 2, ActionType.WAIT,
                          start_position=[1, 0],
                          end_position=[0, 1])) == 't: 1 Agent ID: 2, action: WAIT start:[1 0] end:[0 1]'


class TestPlan:
    def test_getters(self, generic_scenario):
        plan = Plan(generic_scenario, [
            Action(timestep=0, subject_id=1, action_type=ActionType.MOVE, start_position=[0, 1], end_position=[2, 0]),
            Action(timestep=1, subject_id=2, action_type=ActionType.WAIT)])

        assert [agent.id for agent in plan.scenario.agents] == [1, 2]

        assert plan.agent_plans == {
            Agent(1, np.array([0, 0]), np.array([0, 0])): [
                Action(timestep=0, subject_id=1, action_type=ActionType.MOVE, start_position=[0, 1],
                       end_position=[2, 0])],
            Agent(2, [0, 0], [0, 0]): [Action(timestep=1, subject_id=2, action_type=ActionType.WAIT)]
        }

        print([str(action) for action in plan.agent_plan_by_id(1)])
        assert plan.agent_plan_by_id(1).tolist() == [
            Action(timestep=0, subject_id=1, action_type=ActionType.MOVE, start_position=[0, 1], end_position=[2, 0])]
        assert plan.agent_plan_by_id(3) is None

    def test_init_guards(self, generic_scenario):
        with pytest.raises(ValueError) as e:
            plan = Plan(generic_scenario, [Action(timestep=0, subject_id=3, action_type=ActionType.MOVE)])
        assert str(e.value) == "Agent 3 not present in scenario"

        with pytest.raises(ValueError) as e:
            plan = Plan(generic_scenario, [
                Action(timestep=0, subject_id=1, action_type=ActionType.MOVE, start_position=[11, 11],
                       end_position=[0, 0])])
        assert str(e.value).startswith("Invalid start position for action")

        with pytest.raises(ValueError) as e:
            plan = Plan(generic_scenario, [
                Action(timestep=0, subject_id=1, action_type=ActionType.MOVE, start_position=[0, 0],
                       end_position=[11, 11])])
        assert str(e.value).startswith("Invalid end position for action")


    def test_metadata(self, generic_scenario):
        plan = Plan(generic_scenario, [
            Action(timestep=0, subject_id=1, action_type=ActionType.MOVE, start_position=[0, 1], end_position=[2, 0]),
            Action(timestep=1, subject_id=2, action_type=ActionType.WAIT)])

        assert not plan.metadata["solved"]
