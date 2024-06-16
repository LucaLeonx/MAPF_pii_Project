from typing import Optional

import numpy as np

from mapfbench.description import Action, Scenario, Plan, ActionType
from mapfbench.utils.utils import position_not_null


class PlanRecorder:

    def __init__(self, scenario: Scenario, solver: Optional[str] = None):
        self._scenario = scenario
        self._action_list = np.empty(0, dtype=Action)
        self._is_solved = False
        self._solver = solver
        self._agent_positions = dict([(agent.id, agent.start_position) for agent in scenario.agents])

    @property
    def scenario(self) -> Scenario:
        return self._scenario

    @property
    def actions(self) -> np.array:
        return self._action_list

    @property
    def is_solved(self) -> bool:
        return self._is_solved

    @property
    def plan(self):
        return Plan(self._scenario, self._action_list, is_solved=self._is_solved, solver=self._solver)

    def record(self, action):
        if action.subject_id not in self.scenario.agent_ids:
            raise ValueError("No agent with id {} in scenario".format(action.subject_id))

        self._action_list = np.append(self._action_list, action)
        if position_not_null(action.end_position):
            self._agent_positions.update({action.subject_id: action.end_position})

    def record_move(self, timestep: int, agent_id: int, end_position: np.array):
        self.record(Action(timestep, agent_id, ActionType.MOVE,
                           start_position=self._agent_positions[agent_id],
                           end_position=end_position))

    def record_wait(self, timestep: int, agent_id: int):
        self.record(Action(timestep, agent_id, ActionType.WAIT,
                           start_position=self._agent_positions[agent_id],
                           end_position=self._agent_positions[agent_id]))

    def mark_as_solved(self):
        self._is_solved = True
