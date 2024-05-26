import pytest

from description.entity_description import EntityDescription
from description.map.graph import Node
from exceptions import EmptyElementException


class TestEntityDescription:

    @pytest.fixture
    def entity_description(self):
        return EntityDescription("A1", start_position=Node(1))

    @pytest.fixture
    def no_position_entity(self):
        return EntityDescription("E")

    def test_init_guards(self):
        with pytest.raises(EmptyElementException) as excinfo:
            entity = EntityDescription("", start_position=Node(1))
        assert "Entity name cannot be empty" in str(excinfo.value)

        with pytest.raises(EmptyElementException) as excinfo:
            entity = EntityDescription("    ", start_position=Node(2))
        assert "Entity name cannot be empty" in str(excinfo.value)

    def test_get_name(self, entity_description):
        assert entity_description.name == "A1"

    def test_get_start_position(self, entity_description, no_position_entity):
        assert entity_description.start_position == Node(1)
        assert not no_position_entity.has_start_position()

    def test_has_start_position(self, entity_description, no_position_entity):
        assert entity_description.has_start_position()
        assert not no_position_entity.has_start_position()
