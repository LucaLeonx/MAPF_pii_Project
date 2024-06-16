"""
    Module for representing a plan to solve a specific test scenario
"""

from enum import Enum
from typing import Optional

import numpy as np

from mapfbench.description.scenario import Scenario, Agent, AgentReference


class ActionType(Enum):
    """
        Possible types of actions
    """
    WAIT = 0,
    MOVE = 1


class Action:
    """
        Represents an action performed by an Agent as part of the plan
    """

    def __init__(self, timestep: int, subject_id: int, action_type: ActionType,
                 start_position: Optional[np.array] = None,
                 end_position: Optional[np.array] = None):
        """
            Object initialization

            Parameters
            ----------
            timestep : int
                The timestep at which the action is performed.
                Must be non-negative
            subject_id : int
                The ID of the Agent performing the action
            action_type : ActionType
                The type of action performed
            start_position: Optional[np.array]
                The starting position of the agent before the action
            end_position: Optional[np.array]
                The end position of the agent after the action

            Raises
            ------
            ValueError
                If the supplied timestep is negative
        """
        if timestep < 0:
            raise ValueError("Cannot use negative timestep in Action")

        self._timestep = timestep
        self._subject_id = subject_id
        self._action_type = action_type
        self._start_position = np.array(start_position)
        self._end_position = np.array(end_position)

    @property
    def timestep(self) -> int:
        """
            The timestep at which the action is performed
        """
        return self._timestep

    @property
    def subject_id(self) -> int:
        """
            The ID of the Agent performing the Action
        """
        return self._subject_id

    @property
    def action_type(self) -> ActionType:
        """
            The type of action performed by the agent
        """
        return self._action_type

    @property
    def start_position(self) -> Optional[np.array]:
        """
            The starting position of the agent before the action
        """
        return self._start_position

    @property
    def end_position(self) -> Optional[np.array]:
        """
            The ending position of the agent before the action
        """
        return self._end_position

    def __eq__(self, other):
        """
            Equality comparison. Two Actions are equal
            if and only if they have the same timestep, subject_id and action_type.

            Returns
            -------
            bool
                True if the Action have the same timestep, subject ID dnd type
        """
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
    """
        Represents a plan to solve a specified Scenario
        The plan comprises the actions performed by each agent.
    """

    def __init__(self, scenario: Scenario, actions: np.ndarray[Action], is_solved: bool, running_time: float = None,
                 memory_used: float = None):
        """
        Parameters
        ----------
        scenario : Scenario
            The scenario solved by the plan
        actions: List[Action]
            The actions taken by the agents in the plan
        is_solved : bool
            Whether the plan solves the scenario, that is all the agents
            reach their objective position
        running_time: float, optional
            The running time in ms of the algorithm which produced the plan, if available
        memory_used
            The maximum memory used in Kb by the algorithm which produced the plan, if available

        Raises
        ------
        ValueError
            If at least one of the following conditions holds:
                - One of the actions supplied is performed by an agent
                not present in the scenario
                - One of the actions supplied has a start or end position
                not present in the map of the scenario
        """
        for action in actions:
            if action.subject_id not in scenario.agent_ids:
                raise ValueError(f"Agent {action.subject_id} not present in scenario")
            elif action.start_position is not None and not np.array_equal(action.start_position, np.array(
                    None)) and not scenario.map.has_position(action.start_position):
                raise ValueError(f"Invalid start position for action {action}")
            elif action.end_position is not None and not np.array_equal(action.end_position, np.array(
                    None)) and not scenario.map.has_position(action.end_position):
                raise ValueError(f"Invalid end position for action {action}")

        self._scenario = scenario
        self._agent_plans = {}
        self._is_solved = is_solved
        self._running_time = running_time
        self._memory_used = memory_used

        for agent in scenario.agents:
            self._agent_plans[agent] = np.array([action for action in actions if action.subject_id == agent.id], dtype=Action)

    @property
    def scenario(self) -> Scenario:
        """
            The scenario solved by the plan
        """
        return self._scenario

    @property
    def actions(self) -> np.array:
        """
            The list of the actions taken by the agents as part of the plans
        """
        return np.concatenate(self._agent_plans.values(), dtype=Action)

    @property
    def agent_plans(self) -> dict[Agent, list[Action]]:
        """
            The plans of the agents, taken separately

            Returns
            -------
            dict[Agent, list[Action]]
                A dictionary with the agents on the map as keys
                and the list of actions they perform as values
        """
        return self._agent_plans

    @property
    def is_solved(self) -> bool:
        """
            Whether the plan solves the scenario, that is all the agents
            reach their objective position
        """
        return self._is_solved

    @property
    def running_time(self) -> Optional[float]:
        """
            The running time in ms of the algorithm which computed the plan,
            if available
        """
        return self._running_time

    @property
    def memory_used(self) -> Optional[float]:
        """
            The memory usage in KB of the algorithm which computed the plan,
            if available
        """
        return self._memory_used

    def agent_plan_by_id(self, agent_id: int) -> np.array:
        """
            Returns the actions of the agent with the specified ID.
            If no agent with the given ID exists, None is returned

            Parameters
            ----------
            agent_id : int
                The ID of the agent whose actions are sought

            Returns
            -------
            list[Action], optional
                The list with the actions of the agent, None
                if the agent with the given ID does not exist
        """
        return self._agent_plans.get(AgentReference(agent_id), None)
