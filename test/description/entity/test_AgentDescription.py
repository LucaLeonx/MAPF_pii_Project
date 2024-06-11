import pytest

from description.entity_description import AgentDescription, EntityDescription
from description.graph import Node


class TestAgentDescription:

    @pytest.fixture
    def agent_description(self):
        return AgentDescription("A1", "O1", start_position=Node(10))

    def test_init_guards(self):
        with pytest.raises(ValueError) as excinfo:
            agent = AgentDescription("A2", "")
        assert "Agent's objective name cannot be empty" in str(excinfo)

    def test_get_objective(self, agent_description):
        assert agent_description.objective_name == "O1"

    def test_to_dict(self):
        agent_1 = AgentDescription("A1", "O1", start_position=Node(3))
        assert agent_1.to_dict() == {"type": "AgentDescription",
                                     "name": "A1",
                                     "start_position": {"index": 3},
                                     "objective": "O1"}
        agent_2 = AgentDescription("A2", "O2")
        assert agent_2.to_dict() == {"type": "AgentDescription",
                                     "name": "A2",
                                     "objective": "O2"}

    def test_from_dict(self):
        agent_1_dict = {"type": "AgentDescription", "name": "A1", "start_position": {"index": 3}, "objective": "O1"}
        agent_1 = EntityDescription.from_dict(agent_1_dict)
        assert isinstance(agent_1, AgentDescription)
        assert agent_1.name == "A1"
        assert agent_1.has_start_position()
        assert agent_1.start_position == Node(3)
        assert agent_1.objective_name == "O1"

        agent_2_dict = {"type": "AgentDescription", "name": "A2", "objective": "O2"}
        agent_2 = EntityDescription.from_dict(agent_2_dict)
        assert not agent_2.has_start_position()


