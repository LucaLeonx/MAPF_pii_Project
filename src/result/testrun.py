from benchmark.testdescription import TestDescription
from result.action import Action


class TestRun(object):

    # TODO add Runtime information
    def __init__(self, test_description, action_list, is_solved):
        self._test_description = test_description
        self._action_list = action_list
        self._is_solved = is_solved

    @property
    def test_description(self):
        return self._test_description

    @property
    def action_list(self):
        return self._action_list

    @property
    def is_solved(self):
        return self._is_solved

    def to_dict(self, use_coordinates=False):
        return {"test_description": self.test_description.to_dict(use_coordinates=use_coordinates),
                "action_list": [action.to_dict(use_coordinates=use_coordinates) for action in self.action_list],
                "is_solved": self.is_solved}

    @staticmethod
    def from_dict(dictionary, use_coordinates=False):
        return TestRun(TestDescription.from_dict(dictionary["test_description"], use_coordinates),
                       [Action.from_dict(action, use_coordinates) for action in dictionary["action_list"]],
                       dictionary["is_solved"])
