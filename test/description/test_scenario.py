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

    def test_equality(self):
        agent1 = Agent(1, (0, 0), (0, 1))
        agent2 = Agent(2, (0, 0), (0, 1))
        agent3 = Agent(1, (0, 1), (0, 2))
        assert agent1 != agent2
        assert agent1 == agent3


class TestScenario:
    def test_getters(self, generic_scenario):

        scenario = generic_scenario
        # We don't care for positions
        assert scenario.agents == [Agent(1, (0, 0), (0, 0)),
                                   Agent(2, (0, 0), (0, 0))]

        assert scenario.agent_ids == [1, 2]
        assert scenario.agents_num == 2
        assert np.array_equal(scenario.start_positions, np.array([[0, 1], [0, 2]]))
        assert np.array_equal(scenario.objective_positions, np.array([[1, 0], [2, 0]]))
        assert np.array_equal(scenario.map.obstacles, np.array([[0, 1], [1, 1]]))

    def test_from_position_lists(self, generic_map_scheme):
        scenario = Scenario.from_position_lists(generic_map_scheme,
                                                [(0, 2), (2, 1)],
                                                [(0, 0), (0, 2)])
        assert scenario.agents == [Agent(1, (0, 1), (1, 0)),
                                   Agent(2, (0, 2), (2, 0))]

        assert scenario.start_positions.tolist() == [[0, 2], [2, 1]]
        assert scenario.objective_positions.tolist() == [[0, 0], [0, 2]]

        assert np.array_equal(scenario.map.obstacles, np.array([[0, 1], [1, 1]]))

    def test_init_guards(self, generic_map_scheme):
        with pytest.raises(ValueError) as e:
            scenario = Scenario(generic_map_scheme,
                                [Agent(1, (11, 11), (0, 0))])
        assert str(e.value) == "Start position of one of the agents is not present in map"

        with pytest.raises(ValueError) as e:
            scenario = Scenario(generic_map_scheme,
                                [Agent(1, (0, 0), (11, 11))])
        assert str(e.value) == "Objective position of one of the agents is not present in map"
