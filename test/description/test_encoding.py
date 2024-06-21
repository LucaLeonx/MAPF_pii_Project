import msgpack
import numpy as np
import pytest

from mapfbench.description import MapScheme, scenario, Scenario, Plan, ActionType


def test_mapscheme_encoding(generic_map_scheme):
    dictionary = generic_map_scheme.encode()
    assert list(dictionary.keys()) == ["type", "contents"]
    assert dictionary["type"] == "GridMap"
    assert dictionary["contents"] == [[0, -1, 0],
                                      [0, -1, 0],
                                      [0, 0, 0]]
    byte_repr = msgpack.dumps(dictionary)
    new_map = MapScheme.decode(msgpack.loads(byte_repr))
    assert np.array_equal(new_map.contents, generic_map_scheme.contents)


def test_scenario_encoding(generic_scenario):
    dictionary = generic_scenario.encode()
    assert list(dictionary.keys()) == ["type", "map_scheme", "agents", "metadata"]
    assert dictionary["type"] == "Scenario"
    assert dictionary["map_scheme"] == generic_scenario.map.encode()
    byte_repr = msgpack.dumps(dictionary)
    new_scenario = Scenario.decode(msgpack.loads(byte_repr))
    assert np.array_equal(new_scenario.map.contents, generic_scenario.map.contents)
    assert new_scenario.agents_num == generic_scenario.agents_num
    assert new_scenario.agent_ids == generic_scenario.agent_ids
    assert new_scenario.metadata == generic_scenario.metadata


def test_plan_encoding(generic_plan):
    dictionary = generic_plan.encode()
    assert list(dictionary.keys()) == ["type", "scenario", "actions", "metadata"]
    assert dictionary["type"] == "Plan"
    assert dictionary["scenario"] == generic_plan.scenario.encode()
    byte_repr = msgpack.dumps(dictionary)
    new_plan = Plan.decode(msgpack.loads(byte_repr))
    assert np.array_equal(new_plan.scenario.map.contents, new_plan.scenario.map.contents)
    assert new_plan.actions.size == generic_plan.actions.size
    assert new_plan.scenario.agent_ids == generic_plan.scenario.agent_ids
    assert new_plan.metadata == generic_plan.metadata

    print([str(action) for action in new_plan.actions if action.action_type == ActionType.MOVE])
