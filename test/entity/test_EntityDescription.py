import pytest

from entity.entity_description import EntityDescription
from graph.node import Node


class TestEntityDescription:

    @pytest.fixture
    def entity_description(self):
        return EntityDescription("A1", start_position=Node(1))

    @pytest.fixture
    def no_position_entity(self):
        return EntityDescription("E")

    def test_init_guards(self):
        with pytest.raises(ValueError) as excinfo:
            entity = EntityDescription("", start_position=Node(1))
        assert "Name cannot be empty" in str(excinfo.value)

    def test_get_name(self, entity_description):
        assert entity_description.get_name() == "A1"

    def test_get_start_position(self, entity_description, no_position_entity):
        assert entity_description.get_start_position().get() == Node(1)
        assert no_position_entity.get_start_position().is_empty()

    def test_has_start_position(self, entity_description, no_position_entity):
        assert entity_description.has_start_position()
        assert not no_position_entity.has_start_position()
