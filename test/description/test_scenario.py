import pytest
import numpy as np

from mapfbench.description.mapscheme import MapScheme
from mapfbench.description.scenario import Agent, Scenario


class TestAgent:

    def test_init_guards(self):
        with pytest.raises(ValueError) as e:
            agent = Agent(0, (0, 0), (1, 0))
        assert str(e.value) == "Agent ID must be positive"

        with pytest.raises(ValueError) as e:
            agent = Agent(-1, (0, 1), (0, 0))
        assert str(e.value) == "Agent ID must be positive"

        with pytest.raises(ValueError) as e:
            agent = Agent(1, (-1, 10), (0, 0))
        assert str(e.value) == "Invalid negative coordinate in start_position: (-1, 10)"

        with pytest.raises(ValueError) as e:
            agent = Agent(1, (1, 0), (0, -5))
        assert str(e.value) == "Invalid negative coordinate in objective_position: (0, -5)"

    def test_getters(self):
        agent = Agent(3, (0, 4), (5, 6))
        assert agent.id == 3
        assert np.array_equal(agent.start_position, np.array([0, 4]))
        assert np.array_equal(agent.objective_position, np.array([5, 6]))


@pytest.fixture(autouse=True)
def generic_map_scheme():
    return MapScheme(np.array([[0, -1, 0],
                               [0, -1, 0],
                               [0,  0, 0]]))


class TestScenario:
    def test_getters(self, generic_map_scheme):
        scenario = Scenario(generic_map_scheme, [Agent(1, (0, 2), (2, 0)),
                                                 Agent(2, (1, 0), (0, 1))])
        scenario = Scenario.from_position_lists(generic_map_scheme, [(0, 2), (2, 1)], [(0, 0), (0, 2)])
        assert scenario.agents == [Agent(1, (0, 1), (1, 0)),
                                   Agent(2, (0, 2), (2, 0))]
        assert scenario.objective_positions == [(1, 0), (2, 0)]
        assert scenario.start_positions == [(0, 1), (0, 1)]
        assert np.array_equal(scenario.map.obstacles, np.array([[0, 1], [1, 0]]))

