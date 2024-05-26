from description.entity_description import *
from description.map.graph import Graph
from exceptions import DuplicateElementException, EmptyElementException


class BenchmarkDescription:

    def __init__(self, name, tests, description=""):
        if tests is None or len(tests) == 0:
            raise EmptyElementException("Benchmark must have at least one test")
        if name.strip() == "":
            raise EmptyElementException("Benchmark name cannot be empty")

        # Check if all tests have distinct names
        if len(set(tests)) != len(tests):
            raise DuplicateElementException("Added the same test twice")

        self._name = name
        self._description = description
        self._tests = tests

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def tests(self):
        return self._tests

    def __str__(self):
        string = self._name + ": " + self._description + "\n"
        for test in self._tests:
            string += test.__str__()

        return string

    def to_dict(self):
        return {"name": self._name,
                "description": self._description,
                "tests": [test.to_dict() for test in self.tests]}

    @staticmethod
    def from_dict(dictionary):
        return BenchmarkDescription(dictionary["name"],
                                    [TestDescription.from_dict(test) for test in dictionary["tests"]],
                                    dictionary["description"])


class TestDescription:

    def __init__(self, name, graph, entities):
        if name.strip() == "":
            raise EmptyElementException("Test name cannot be empty")

        self._name = name
        self._graph = graph
        self._entities = entities

    @property
    def name(self):
        return self._name

    @property
    def graph(self):
        return self._graph

    @property
    def entities(self):
        return self._entities

    def _get_entities_by_class(self, selected_class):
        return [entity for entity in self._entities if isinstance(entity, selected_class)]

    @property
    def agents(self):
        return self._get_entities_by_class(AgentDescription)

    @property
    def obstacles(self):
        return self._get_entities_by_class(ObstacleDescription)

    @property
    def objectives(self):
        return self._get_entities_by_class(ObjectiveDescription)

    def __eq__(self, other):
        if isinstance(other, TestDescription):
            return self.name == other.name
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        string = self.name + ":\n" + "Map: \n" + str(self.graph) + "\n"
        for entity in self._entities:
            string += str(entity) + "\n"
        return string

    def to_dict(self, use_coords=False):
        return {"name": self.name,
                "graph": self.graph.to_dict(use_coords),
                "entities": [entity.to_dict(use_coords) for entity in self.entities]}

    @staticmethod
    def from_dict(dictionary):
        return TestDescription(dictionary["name"],
                               Graph.from_dict(dictionary["graph"]),
                               [EntityDescription.from_dict(entity_dict) for entity_dict in dictionary["entities"]])
