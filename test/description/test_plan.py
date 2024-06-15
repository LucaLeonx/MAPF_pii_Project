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


class TestPlan:
    def test_getters(self, generic_scenario):
        plan = Plan(generic_scenario, [
            Action(timestep=0, subject_id=1, action_type=ActionType.MOVE, start_position=[0, 1], end_position=[2, 0]),
            Action(timestep=1, subject_id=2, action_type=ActionType.WAIT)],
                    is_solved=True, solver="CBS")

        assert [agent.id for agent in plan.scenario.agents] == [1, 2]
        assert plan.is_solved
        assert plan.solver == "CBS"

        # TODO fix these testes
        '''
        assert plan.agent_plans == {
            Agent(1, np.array([0, 0]), np.array([0, 0])): [
                Action(timestep=0, subject_id=1, action_type=ActionType.MOVE, start_position=[0, 1],
                       end_position=[2, 0])],
            Agent(2, [0, 0], [0, 0]): [Action(timestep=1, subject_id=2, action_type=ActionType.WAIT)]
        }
        '''

        assert plan.agent_plan_by_id(1).tolist() == [
            Action(timestep=0, subject_id=1, action_type=ActionType.MOVE, start_position=[0, 1], end_position=[2, 0])]
        assert plan.agent_plan_by_id(3) is None

    def test_init_guards(self, generic_scenario):
        with pytest.raises(ValueError) as e:
            plan = Plan(generic_scenario, [Action(timestep=0, subject_id=3, action_type=ActionType.MOVE)],
                        is_solved=False)
        assert str(e.value) == "Agent 3 not present in scenario"

        with pytest.raises(ValueError) as e:
            plan = Plan(generic_scenario, [Action(timestep=0, subject_id=1, action_type=ActionType.MOVE, start_position=[11, 11], end_position=[0, 0])],
                        is_solved=False)
        assert str(e.value).startswith("Invalid start position for action")

        with pytest.raises(ValueError) as e:
            plan = Plan(generic_scenario, [Action(timestep=0, subject_id=1, action_type=ActionType.MOVE, start_position=[0, 0], end_position=[11, 11])],
                        is_solved=False)
        assert str(e.value).startswith("Invalid end position for action")
