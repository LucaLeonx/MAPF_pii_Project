import pytest

from entity.agent_description import AgentDescription
from entity.objective_description import ObjectiveDescription
from graph.node import Node


class TestAgentDescription:

    @pytest.fixture
    def agent_description(self):
        return AgentDescription("A1", start_position=Node(10), objective=ObjectiveDescription("O1", start_position=Node(2)))

    def test_init_guards(self):
        with pytest.raises(ValueError) as excinfo:
            agent = AgentDescription("A2")
        assert "Objective of the agent must be declared" in str(excinfo)

    def test_get_objective(self, agent_description):
        objective = agent_description.get_objective()
        assert objective.get_name() == "O1"
        assert objective.get_start_position().get() == Node(2)

