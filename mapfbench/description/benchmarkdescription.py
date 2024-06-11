from description.entity_description import *
from typing import Any, List, Dict, Optional
from utilities.customexceptions import EmptyElementException, InvalidElementException
from description.graph import Graph


class TestDescription:
    """
        The description of a test instance
    """
    def __init__(self, name: str, graph: Graph, entities: List[EntityDescription]):
        """
            Object initializer

            Parameters
            ----------
            name: str
                The identifying name of the test
            graph: Graph
                The graph representing the map of the test
            entities: List[EntityDescription]
                The entities considered in the test

            Raises
            ------
            EmptyElementException
                If the name of the test is a whitespace only string
        """
        if name.strip() == "":
            raise EmptyElementException("Test name cannot be empty")

        self._name = name
        self._graph = graph
        self._entities = entities

    @property
    def name(self) -> str:
        """
            The name of the test
        """
        return self._name

    @property
    def graph(self) -> Graph:
        """
            The graph representing the map of the test
        """
        return self._graph

    @property
    def entities(self) -> List[EntityDescription]:
        """
            The entities considered in the test
        """
        return self._entities

    def _get_entities_by_class(self, selected_class):
        return [entity for entity in self._entities if isinstance(entity, selected_class)]

    @property
    def agents(self) -> List[AgentDescription]:
        """
            The agents considered in the test
        """
        return self._get_entities_by_class(AgentDescription)

    @property
    def objectives(self) -> List[ObjectiveDescription]:
        """
            The objectives considered in the test
        """
        return self._get_entities_by_class(ObjectiveDescription)

    @property
    def obstacles(self) -> List[ObstacleDescription]:
        """
            The obstacles considered in the test
        """
        return self._get_entities_by_class(ObstacleDescription)

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
    """
        The description of a benchmark
    """
    def __init__(self, name: str, tests: Dict[TestDescription, int]):
        """
            Object initializer

            Parameters
            ----------
            name: str
                The identifying name of the benchmark
            tests: Dict[TestDescription, int]
                The tests comprising the benchmark, with the corresponding number of iterations

            Raises
            ------
            EmptyElementException
                If the name of the benchmark is a whitespace only string
            InvalidElementException
                If an empty group of tests has been supplied or the number of
                iterations of a test is invalid (zero or negative)
        """
        if tests is None or len(tests) == 0:
            raise InvalidElementException("Benchmark must have at least one test")
        if any([occurrences <= 0 for occurrences in tests.values()]):
            raise InvalidElementException("Number of occurrences for each test must be positive")
        if name.strip() == "":
            raise EmptyElementException("Benchmark name cannot be empty")

        self._name = name
        self._tests = tests

    @property
    def name(self) -> str:
        """
            The name of the benchmark
        """
        return self._name

    @property
    def tests(self) -> List[TestDescription]:
        """
            The tests comprising the benchmark
        """
        return list(self._tests.keys())

    @property
    def test_occurrences(self) -> Dict[TestDescription, int]:
        """
            The tests comprising the benchmark, along with their number of iterations
        """
        return self._tests

    def get_test_by_name(self, test_name: str) -> Optional[TestDescription]:
        """
            Returns the test with the given name

            Parameters
            ----------
            test_name: str
                The name of the requested test

            Returns
            -------
            TestDescription
                The description of the requested test. None if not found
        """
        return next(test for test in self.tests if test.name == test_name)

    def get_test_occurrences(self, test_name: str) -> int:
        """
            Returns the number of iterations of the test with the given name

            Parameters
            ----------
            test_name: str
                The name of the requested test

            Returns
            -------
            int
                The number of iterations of the test with the given name. 0 is returned if the test is not found
        """
        test_description = self.get_test_by_name(test_name)

        if test_description:
            return self.test_occurrences[test_description]
        else:
            return 0

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
