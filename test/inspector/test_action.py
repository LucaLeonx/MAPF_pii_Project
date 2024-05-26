import pytest

from graph.node import Node
from result.action import Action, MoveAction, AppearAction, DisappearAction, WaitAction
from exceptions import ElementNotAvailableException

action = Action(3, "A1", Node(coordinates=(1, 0)))
move = MoveAction(1, "A2", Node(coordinates=(10, 0)))
wait = WaitAction(1, "A2")
appear = AppearAction(0, "A2", Node(coordinates=(0, 0)))
disappear = DisappearAction(5, "A2")
custom_action = Action(10, "A5", Node(coordinates=(10, 10)), description="AstralTeleport")


class TestAction:

    def test_getters(self):

        assert action.timestep == 3
        assert move.subject == "A2"
        assert appear.position == Node(coordinates=(0, 0))

        assert action.description == ""
        assert move.description == "Move"
        assert wait.description == "Wait"
        assert appear.description == "Appear"
        assert disappear.description == "Disappear"
        assert custom_action.description == "AstralTeleport"

        with pytest.raises(ElementNotAvailableException) as excinfo:
            print(disappear.position)
        assert "This action doesn't have a final position" in str(excinfo)

    def test_to_dict(self):

        assert action.to_dict(use_coordinates=True) == {
            "type": "Action",
            "timestep": 3,
            "subject": "A1",
            "position": {"x": 1, "y": 0},
            "description": ""
        }

        assert wait.to_dict() == {
            "type": "WaitAction",
            "timestep": 1,
            "subject": "A2",
            "description": "Wait"
        }

        assert appear.to_dict() == {
            "type": "AppearAction",
            "timestep": 0,
            "subject": "A2",
            "position": {"index": 0},
            "description": "Appear"
        }

    def test_from_dict(self):
        assert Action.from_dict(action.to_dict()).position == Node(coordinates=(1, 0))
        assert (Action.from_dict(move.to_dict(use_coordinates=True), use_coordinates=True).__class__.__name__
                == "MoveAction")

        appear_duplicate = Action.from_dict({
            "type": "AppearAction",
            "timestep": 0,
            "subject": "A2",
            "position": {"index": 0},
            "description": "Appear"
        })

        assert appear_duplicate.__class__ == appear.__class__
        assert appear_duplicate.timestep == appear.timestep
        assert appear_duplicate.subject == appear.subject
        assert appear_duplicate.position == appear.position
        assert appear_duplicate.description == appear.description
