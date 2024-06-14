import numpy as np

from mapfbench.description.mapscheme import MapScheme


class Agent:
    def __init__(self, agent_id: int, start_position: tuple[int, int], objective_position: tuple[int, int]):
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
        return self._id

    @property
    def start_position(self) -> np.array:
        return self._start_position

    @property
    def objective_position(self) -> np.array:
        return self._objective_position

    def __eq__(self, other):
        if isinstance(other, Agent):
            return self.id == other.id

    def __str__(self):
        return f"Agent: {self}, start_position: {self.start_position}, objective_position: {self.objective_position}"


class Scenario:
    def __init__(self, map_scheme: MapScheme, agents: list[Agent]):
        if any(not map_scheme.has_position(agent.start_position) for agent in agents):
            raise ValueError(f"Start position of agents is not present in map")
        elif any(not map_scheme.has_position(agent.objective_position) for agent in agents):
            raise ValueError(f"Objective position of agents is not present in map")

        self._map_scheme = map_scheme
        self._agents = list(agents)
        self._agents.sort(key=lambda agent: agent.id)

    @staticmethod
    def from_position_lists(map_scheme: MapScheme, start_positions: list[tuple[int, int]], objective_positions: list[tuple[int, int]]):
        agents = []
        next_id = 1

        for start_position, objective_position in zip(start_positions, objective_positions):
            agents.append(Agent(next_id, start_position, objective_position))
            next_id += 1

        return Scenario(map_scheme, agents)

    @property
    def map(self) -> MapScheme:
        return self._map_scheme

    @property
    def agents(self) -> list[Agent]:
        return self._agents

    @property
    def start_positions(self) -> np.array:
        return np.array([agent.start_position for agent in self._agents])

    @property
    def objective_positions(self) -> np.array:
        return np.array([agent.objective_position for agent in self._agents])





