from description.entity_description import *
from description.map.graph import Graph, GridGraph
from exceptions import DuplicateElementException, EmptyElementException, InvalidElementException

from typing import Any, List, Dict


class TestDescription:

    def __init__(self, name: str, graph: Graph, entities: List[EntityDescription]):
        if name.strip() == "":
            raise EmptyElementException("Test name cannot be empty")

        self._name = name
        self._graph = graph
        self._entities = entities

    @property
    def name(self) -> str:
        return self._name

    @property
    def graph(self) -> Graph:
        return self._graph

    @property
    def entities(self) -> List[EntityDescription]:
        return self._entities

    def _get_entities_by_class(self, selected_class):
        return [entity for entity in self._entities if isinstance(entity, selected_class)]

    @property
    def agents(self) -> List[AgentDescription]:
        return self._get_entities_by_class(AgentDescription)

    @property
    def obstacles(self) -> List[ObstacleDescription]:
        return self._get_entities_by_class(ObstacleDescription)

    @property
    def objectives(self) -> List[ObjectiveDescription]:
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

    def to_dict(self):
        return {"name": self.name,
                "graph": self.graph.to_dict(),
                "entities": [entity.to_dict() for entity in self.entities]}

    @staticmethod
    def from_dict(dictionary):
        return TestDescription(dictionary["name"],
                               Graph.from_dict(dictionary["graph"]),
                               [EntityDescription.from_dict(entity_dict) for entity_dict in dictionary["entities"]])

class BenchmarkDescription:

    def __init__(self, name: str, tests: dict[TestDescription, int]):
        if tests is None or len(tests) == 0:
            raise EmptyElementException("Benchmark must have at least one test")
        if any([occurrences <= 0 for occurrences in tests.values()]):
            raise InvalidElementException("Number of occurrences for each test must be positive")
        if name.strip() == "":
            raise EmptyElementException("Benchmark name cannot be empty")

        self._name = name
        self._tests = tests

    @property
    def name(self) -> str:
        return self._name

    @property
    def tests(self) -> List[TestDescription]:
        return list(self._tests.keys())

    @property
    def test_occurrences(self) -> Dict[TestDescription, int]:
        return self._tests

    def get_test_by_name(self, test_name) -> TestDescription:
        return next(test for test in self.tests if test.name == test_name)

    def get_test_occurrences(self, test_name) -> int:
        return self.test_occurrences[self.get_test_by_name(test_name)]

    def __str__(self):
        string = self.name + "\n"
        for test in self.tests:
            string += str(test)

        return string

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self._name,
                "test_occurrences": dict(map(lambda item: (item[0].name, item[1]), self.test_occurrences.items())),
                "tests": [test.to_dict() for test in self.tests]}

    @staticmethod
    def from_dict(dictionary: Dict[str, Any]):
        tests = [TestDescription.from_dict(test) for test in dictionary["tests"]]
        test_occurrences = dict()

        for test in tests:
            test_occurrences.update({test: dictionary["test_occurrences"][test.name]})

        return BenchmarkDescription(dictionary["name"], test_occurrences)
