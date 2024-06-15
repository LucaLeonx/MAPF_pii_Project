from enum import IntEnum
from typing import Optional

import numpy as np

from mapfbench.description.scenario import Scenario, Agent, AgentReference


class ActionType(IntEnum):
    WAIT = 0,
    MOVE = 1


class Action:

    def __init__(self, timestep: int, subject_id: int, action_type: ActionType,
                 start_position: Optional[np.array] = None,
                 end_position: Optional[np.array] = None):
        if timestep < 0:
            raise ValueError("Cannot use negative timestep in Action")

        self._timestep = timestep
        self._subject_id = subject_id
        self._action_type = action_type
        self._start_position = np.array(start_position)
        self._end_position = np.array(end_position)

    @property
    def timestep(self) -> int:
        return self._timestep

    @property
    def subject_id(self) -> int:
        return self._subject_id

    @property
    def action_type(self) -> ActionType:
        return self._action_type

    @property
    def start_position(self) -> Optional[np.array]:
        return self._start_position

    @property
    def end_position(self) -> Optional[np.array]:
        return self._end_position

    def __eq___(self, other):
        if isinstance(other, Action):
            return self.timestep == other.timestep and self.subject_id == other.subject_id

    def __hash__(self):
        return hash((self.timestep, self.subject_id))

    def __str__(self):
        string = f"t: {self.timestep} Agent ID: {self.subject_id}, action: {self.action_type}"
        string += f" start:{self.start_position}" if self.start_position is not None else ""
        string += f" end:{self.end_position}" if self.end_position is not None else ""
        return string


class Plan:
    def __init__(self, scenario: Scenario, actions: list[Action], is_solved: bool, solver: Optional[str] = None):
        for action in actions:
            if action.subject_id not in scenario.agent_ids:
                raise ValueError(f"Agent {action.subject_id} not present in scenario")
            elif action.start_position is not None and not np.array_equal(action.start_position, np.array(None)) and not scenario.map.has_position(action.start_position):
                raise ValueError(f"Invalid start position for action {action}")
            elif action.end_position is not None and not np.array_equal(action.end_position, np.array(None)) and not scenario.map.has_position(action.end_position):
                raise ValueError(f"Invalid end position for action {action}")

        self._scenario = scenario
        self._agent_plans = {}
        self._is_solved = is_solved
        self._solver = solver

        for agent in scenario.agents:
            self._agent_plans[agent] = np.array([action for action in actions if action.subject_id == agent.id])

    @property
    def scenario(self) -> Scenario:
        return self._scenario

    @property
    def actions(self) -> np.array:
        return np.concatenate(self._agent_plans.values())

    @property
    def agent_plans(self) -> dict[Agent, np.array]:
        return self._agent_plans

    @property
    def is_solved(self) -> bool:
        return self._is_solved

    @property
    def solver(self) -> Optional[str]:
        return self._solver

    def agent_plan_by_id(self, agent_id: int) -> np.array:
        return self._agent_plans.get(AgentReference(agent_id), None)
