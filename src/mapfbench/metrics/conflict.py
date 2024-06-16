from abc import ABC

import numpy as np

from mapfbench.description import AgentReference


class Conflict(ABC):

    def __init__(self, timestep: int, agent1_id: int, agent2_id: int):
        self._timestep = timestep
        self._agent1 = AgentReference(agent1_id)
        self._agent2 = AgentReference(agent2_id)

    @property
    def timestep(self) -> int:
        return self._timestep

    @property
    def agent1(self) -> AgentReference:
        return self._agent1

    @property
    def agent2(self) -> AgentReference:
        return self._agent2

    @property
    def agents(self) -> np.array:
        return np.array((self._agent1, self._agent2))


class VertexConflict(Conflict):

    def __init__(self, timestep: int, agent1_id: int, agent2_id: int, position: np.array):
        super().__init__(timestep, agent1_id, agent2_id)
        self._position = np.array(position)

    @property
    def position(self) -> np.ndarray[int]:
        return self._position

    def __str__(self):
        return f"VertexConflict(t: {self.timestep}, agent1: {self.agent1.id}, agent2: {self.agent2.id}, position: {self.position}"


class EdgeConflict(Conflict):
    def __init__(self, timestep: int, agent1_id: int, agent2_id, agent1_start: np.ndarray,
                 agent2_start: np.ndarray[int]):
        super().__init__(timestep, agent1_id, agent2_id)
        self._agent1_start = np.array(agent1_start)
        self._agent2_start = np.array(agent2_start)

    @property
    def agent1_start(self) -> np.ndarray[int]:
        return self._agent1_start

    @property
    def agent2_start(self) -> np.ndarray[int]:
        return self._agent2_start

    @property
    def edge(self) -> np.ndarray:
        return np.array([self._agent1_start, self._agent2_start])

    def __str__(self):
        return f"EdgeConflict(t: {self.timestep}, agent1: {self.agent1.id} (start: {self._agent1_start}), agent2: {self.agent2.id} (start: {self._agent2_start})"


class ObstacleConflict(VertexConflict):

    def __init__(self, timestep: int, agent1_id: int, position: np.array):
        super().__init__(timestep, agent1_id, 1, position)
        self._agent2 = None

    def __str__(self):
        return f"VertexConflict(t: {self.timestep}, agent1: {self.agent1.id}, agent2: obstacle, position: {self.position}"