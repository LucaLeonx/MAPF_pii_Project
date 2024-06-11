import pytest

from description.entity_description import EntityDescription, ObstacleDescription, ObjectiveDescription
from description.graph import Node
from customexceptions import EmptyElementException


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

    def test_to_dict(self):
        entity = EntityDescription("Entity")
        obstacle = ObstacleDescription("Obstacle", start_position=Node(2))
        objective = ObjectiveDescription("Objective", start_position=Node(3))
        assert entity.to_dict() == {"type": "EntityDescription", "name": "Entity"}
        assert obstacle.to_dict() == {"type": "ObstacleDescription", "name": "Obstacle", "start_position": {"index": 2}}
        assert objective.to_dict() == {"type": "ObjectiveDescription", "name": "Objective", "start_position": {"index": 3}}

    def test_from_dict(self):
        dictionary_entity = {"type": "EntityDescription", "name": "Good", "start_position": {"index": 10}}
        entity = EntityDescription.from_dict(dictionary_entity)

        assert entity.name == "Good"
        assert entity.start_position == Node(10)
        assert entity.has_start_position()

        dictionary_obstacle = {"type": "ObstacleDescription", "name": "Bad"}
        obstacle = EntityDescription.from_dict(dictionary_obstacle)
        assert isinstance(obstacle, ObstacleDescription)
        assert obstacle.name == "Bad"
        assert obstacle.start_position is None
        assert not obstacle.has_start_position()

        dictionary_objective = {"type": "ObjectiveDescription", "name": "Nice", "start_position": {"index": 7}}
        objective = EntityDescription.from_dict(dictionary_objective)
        assert isinstance(objective, ObjectiveDescription)
        assert objective.name == "Nice"
        assert objective.start_position == Node(7)
