import time
from typing import Optional

import numpy as np
import psutil

from mapfbench.description import Action, Scenario, Plan, ActionType
from mapfbench.utils.utils import position_not_null


class PlanRecorder:

    def __init__(self, scenario: Scenario):
        self._scenario = scenario
        self._action_list = np.empty(0, dtype=Action)
        self._is_solved = False
        self._agent_positions = dict([(agent.id, agent.start_position) for agent in scenario.agents])
        self._start_time = None,  # In ms
        self._end_time = None
        self._memory_used = None  # In kb
        self._process_reference = None

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
        running_time = None
        memory_used = None
        if self._end_time is not None:
            running_time = (self._end_time - self._start_time) / 1_000_000
            memory_used = self._memory_used / 1024

        plan = Plan(self._scenario, self._action_list)
        plan.metadata["running_time"] = running_time
        plan.metadata["memory_used"] = memory_used

        return plan

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

    def start_profiling(self):
        self._end_time = None
        self._process_reference = psutil.Process()
        self._start_time = time.perf_counter_ns()

    def end_profiling(self):
        if self._process_reference:
            self._memory_used = self._process_reference.memory_info().rss
            self._end_time = time.perf_counter_ns()

