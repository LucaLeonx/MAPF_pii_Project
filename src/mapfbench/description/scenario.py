"""
    Classes used to define a test scenario
"""

import numpy as np

from mapfbench.description.mapscheme import MapScheme


class Agent:
    """
        Represents a single agent on the map
        Agents are uniquely identified by their IDs,
        so the __eq__ comparison checks only them
    """
    def __init__(self, agent_id: int, start_position: tuple[int, int], objective_position: tuple[int, int]):
        """
            Object initialization

            Parameters
            ----------
            agent_id : int
                The identifying number of the agent. Must be strictly positive
            start_position:  np.array
                The initial position of the agent on the map
            objective_position: np.array
                The position of the objective of the agent on the map

            Raises
            ------
            ValueError
                If the specified parameters are invalid, that is at least one of
                the following conditions holds:
                - The ID of the agent is negative or null
                - The start position has at least one negative coordinate
                - The objective position has at least one negative coordinate
        """
        if agent_id <= 0:
            raise ValueError("Agent ID must be positive")
        elif any(coord < 0 for coord in start_position):
            raise ValueError(f"Invalid negative coordinate in start_position: {start_position}")
        elif any(coord < 0 for coord in objective_position):
            raise ValueError(f"Invalid negative coordinate in objective_position: {objective_position}")

        self._id = agent_id
        self._start_position = np.array(start_position)
        self._objective_position = np.array(objective_position)

    @property
    def id(self) -> int:
        """
            The identifying number of the agent
        """
        return self._id

    @property
    def start_position(self) -> np.array:
        """
            The initial position of the agent on the map
        """
        return self._start_position

    @property
    def objective_position(self) -> np.array:
        """
            The objective position of the agent on the map
        """
        return self._objective_position

    def __eq__(self, other):
        """
            Compare two agents for equality.
            Two agents are equal if and only if they have the same ID,
            that is self.id == other.id

            Returns
            -------
            bool
                True if the two agents have the same ID, false otherwise
        """
        if isinstance(other, Agent):
            return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __str__(self):
        return f"Agent: {self}, start_position: {self.start_position}, objective_position: {self.objective_position}"


class AgentReference(Agent):
    """
        Class that represents a reference to an agent, using its ID only.
        Use this class only to refer to an Agent used as key in a collection;
        the getters of start_position and objective_positions are overridden
        to return None.
    """
    def __init__(self, agent_id: int):
        """
            Object initializer

            Parameters
            ----------
            agent_id : int
                The id of the referenced Agent

            Raises
            ------
            ValueError
                If the supplied ID is negative or null
        """
        super().__init__(agent_id, (0, 0), (0, 0))

    @property
    def start_position(self) -> None:
        return None

    @property
    def end_position(self) -> None:
        return None

class Scenario:
    """
        Represents a test scenario, characterized by a map and agents on it
    """
    def __init__(self, map_scheme: MapScheme, agents: list[Agent]):
        """
            Object initializer

            Parameters
            ----------
            map_scheme : MapScheme
                The map to use for the test
            agents: List[Agent]
                The list of Agents considered in the scenario

            Raises
            ------
            ValueError
                If at lest one of the following invalid conditions holds:
                - At least one of the agents has a start position not present on the map
                - At least one of the agents has an objective position not present on the map
        """
        if any(not map_scheme.has_position(agent.start_position) for agent in agents):
            raise ValueError(f"Start position of one of the agents is not present in map")
        elif any(not map_scheme.has_position(agent.objective_position) for agent in agents):
            raise ValueError(f"Objective position of one of the agents is not present in map")

        self._map_scheme = map_scheme
        self._agents = list(agents)
        self._agents.sort(key=lambda agent: agent.id)

    @staticmethod
    def from_position_lists(map_scheme: MapScheme, start_positions: list[tuple[int, int]],
                            objective_positions: list[tuple[int, int]]):
        """
        Generates a scenario from a list of starting positions and objectives.
        The start and objective positions with the same index i in the lists are
        associated to the Agent with ID i+1.
        If the lists have different length, they are truncated at the shortest length

        Parameters
        ----------
        map_scheme : MapScheme
            The map used for the scenario
        start_positions : list[np.array]
            The starting positions of the agents
        objective_positions : list[np.array]
            The objectives positions of the agents

        Returns
        -------
        A Scenario instance, where the map is the provided one
        and the Agents have start position and objectives positions
        associated based on their index in the lists

        Raises
        ------
        ValueError
            If one of the lists contains an invalid position,
            no present in the map
        """
        agents = []
        next_id = 1

        for start_position, objective_position in zip(start_positions, objective_positions):
            agents.append(Agent(next_id, start_position, objective_position))
            next_id += 1

        return Scenario(map_scheme, np.array(agents))

    @property
    def map(self) -> MapScheme:
        """
            The map used for the scenario
        """
        return self._map_scheme

    @property
    def agents(self) -> np.array:
        """
            A list of the agents associated with the scenario
        """
        return self._agents

    @property
    def agent_ids(self) -> list[int]:
        """
            The ids of the agents associated with the scenario
        """
        return [agent.id for agent in self._agents]

    @property
    def agents_num(self) -> int:
        """
            The number of agents associated with the scenario
        """
        return len(self._agents)

    @property
    def start_positions(self) -> np.array:
        """
            The start positions of the agents in the scenario
        """
        return np.array([agent.start_position for agent in self._agents])

    @property
    def objective_positions(self) -> np.array:
        """
            The positions of the objectives in the scenario
        """
        return np.array([agent.objective_position for agent in self._agents])
