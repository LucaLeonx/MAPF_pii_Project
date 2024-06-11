import pytest

from description.graph import Node
from customexceptions import ElementNotAvailableException
from result.action import Action, MoveAction, WaitAction, AppearAction, DisappearAction

action = Action(3, "A1", Node(coords=(1, 0)))
move = MoveAction(1, "A2", Node(coords=(1, 0)), Node(coords=(10, 0)))
wait = WaitAction(1, "A2", Node(coords=(1, 0)))
appear = AppearAction(0, "A2", Node(coords=(0, 0)))
disappear = DisappearAction(5, "A2")
custom_action = Action(10, "A5", Node(coords=(10, 10)), description="AstralTeleport")


class TestAction:

    def test_getters(self):

        assert action.timestep == 3
        assert move.subject == "A2"
        assert appear.end_position == Node(coords=(0, 0))

        assert action.description == ""
        assert move.description == "Move"
        assert wait.description == "Wait"
        assert appear.description == "Appear"
        assert disappear.description == "Disappear"
        assert custom_action.description == "AstralTeleport"

        with pytest.raises(ElementNotAvailableException) as excinfo:
            print(disappear.start_position)
        assert "This action doesn't have a final position" in str(excinfo)

    def test_to_dict(self):

        assert action.to_dict() == {
            "type": "Action",
            "timestep": 3,
            "subject": "A1",
            "start_position": {"index": 1},
            "description": ""
        }

        assert wait.to_dict() == {
            "type": "WaitAction",
            "timestep": 1,
            "subject": "A2",
            "start_position": {"index": 1},
            "description": "Wait"
        }

        assert appear.to_dict() == {
            "type": "AppearAction",
            "timestep": 0,
            "subject": "A2",
            "end_position": {"index": 0},
            "description": "Appear"
        }

    def test_from_dict(self):
        assert Action.from_dict(action.to_dict()).start_position == Node(coords=(1, 0))
        assert (Action.from_dict(move.to_dict()).__class__.__name__
                == "MoveAction")

        appear_duplicate = Action.from_dict({
            "type": "AppearAction",
            "timestep": 0,
            "subject": "A2",
            "end_position": {"index": 0},
            "description": "Appear"
        })

        assert appear_duplicate.__class__ == appear.__class__
        assert appear_duplicate.timestep == appear.timestep
        assert appear_duplicate.subject == appear.subject
        assert appear_duplicate.end_position == appear.end_position
        assert appear_duplicate.description == appear.description
