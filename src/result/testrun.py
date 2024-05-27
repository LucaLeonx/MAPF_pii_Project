from typing import Any

from description.benchmarkdescription import TestDescription
from result.action import Action


class TestRun(TestDescription):

    # TODO add Runtime information
    def __init__(self, test_description, action_list, is_solved):
        super().__init__(test_description.name, test_description.graph, test_description.entities)
        self._test_description = test_description
        self._action_list = action_list
        self._is_solved = is_solved

    @property
    def test_description(self) -> TestDescription:
        return self._test_description

    @property
    def action_list(self) -> list[Action]:
        return self._action_list

    @property
    def is_solved(self) -> bool:
        return self._is_solved

    def to_dict(self) -> dict[str, Any]:
        return {"test_description": self.test_description.to_dict(),
                "number": self._number,
                "action_list": [action.to_dict() for action in self.action_list],
                "is_solved": self.is_solved}

    @staticmethod
    def from_dict(dictionary):
        return TestRun(TestDescription.from_dict(dictionary["test_description"]),
                       dictionary["number"],
                       [Action.from_dict(action) for action in dictionary["action_list"]],
                       dictionary["is_solved"])
