import pytest

from entity.agent_description import AgentDescription
from entity.objective_description import ObjectiveDescription
from graph.node import Node


class TestAgentDescription:

    @pytest.fixture
    def agent_description(self):
        return AgentDescription("A1", "O1", start_position=Node(10), )

    def test_init_guards(self):
        with pytest.raises(ValueError) as excinfo:
            agent = AgentDescription("A2", "")
        assert "Agent's objective name cannot be empty" in str(excinfo)

    def test_get_objective(self, agent_description):
        assert agent_description.get_objective_name() == "O1"

