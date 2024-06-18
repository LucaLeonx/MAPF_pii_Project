import numpy as np
import pytest

from mapfbench.description import AgentReference
from mapfbench.metrics.conflict import VertexConflict, EdgeConflict


class TestConflict:

    def test_vertex_conflict(self):

        conflict = VertexConflict(1, 1, 2, [0, 1])
        assert conflict.timestep == 1
        assert conflict.agent1 == AgentReference(1)
        assert conflict.agent2 == AgentReference(2)
        assert np.array_equal(conflict.agents, np.array((AgentReference(1), AgentReference(2))))
        assert np.array_equal(conflict.position, np.array([0, 1]))

    def test_edge_conflict(self):
        conflict = EdgeConflict(3, 5, 4, np.array([1, 2]), np.array([1, 1]))
        assert conflict.timestep == 3
        assert conflict.agent1 == AgentReference(5)
        assert conflict.agent2 == AgentReference(4)
        assert np.array_equal(conflict.agents, np.array([AgentReference(5), AgentReference(4)]))
        assert np.array_equal(conflict.agent1_start, np.array([1, 2]))
        assert np.array_equal(conflict.agent2_start, np.array([1, 1]))
        assert np.array_equal(conflict.edge, np.array([[1, 2], [1, 1]]))