import numpy as np
import pytest

from mapfbench.description import MapContent, GridMap


@pytest.mark.parametrize("map_contents, "
                         "exp_width, exp_height, "
                         "exp_free_positions, "
                         "exp_obstacles",
                         [([[0, 0, 0],
                            [-1, 0, -1],
                            [0, -1, 0]], 3, 3,
                           [[0, 0], [0, 1], [0, 2], [1, 1], [2, 0], [2, 2]],
                           [[1, 0], [1, 2], [2, 1]]),

                          ([[0, -1, 0],
                            [-1, 0, 0]], 3, 2,
                           [[0, 0], [0, 2], [1, 1], [1, 2]],
                           [[0, 1], [1, 0]]),

                          ([[-1, 0],
                            [0, -1],
                            [0, 0]], 2, 3,
                           [[0, 1], [1, 0], [2, 0], [2, 1]],
                           [[0, 0], [1, 1]]),

                          ([[0, 0],
                            [0, 0]], 2, 2,
                           [[0, 0], [0, 1], [1, 0], [1, 1]],
                           np.array([]).reshape(0, 2)),
                          ([[-1, -1],
                            [-1, -1]], 2, 2,
                           np.array([]).reshape(0, 2),
                           [[0, 0], [0, 1], [1, 0], [1, 1]]),

                          ([[1, 2],
                            [3, 4],
                            [0, -1]], 2, 3,
                           [[2, 0]],
                           [[2, 1]])
                          ])
class TestMapScheme:

    def test_getters(self, map_contents, exp_width, exp_height, exp_free_positions, exp_obstacles):
        map_scheme = GridMap(map_contents)
        assert map_scheme.width == exp_width
        assert map_scheme.height == exp_height

        unrecognized_content = 0

        for i in range(map_scheme.height):
            for j in range(map_scheme.width):
                unrecognized_content += 1 if map_contents[i][j] not in MapContent.values else 0

        assert map_scheme.obstacles.shape[0] + map_scheme.free_positions.shape[0] + unrecognized_content == map_scheme.width * map_scheme.height

        assert np.array_equal(map_scheme.free_positions, np.array(exp_free_positions))
        assert np.array_equal(map_scheme.obstacles, np.array(exp_obstacles))


    def test_has_position(self, map_contents, exp_width, exp_height, exp_free_positions, exp_obstacles):
        map_scheme = GridMap(map_contents)
        assert map_scheme.has_position([0, 0])
        assert not map_scheme.has_position(np.array([10, 1]))
        assert not map_scheme.has_position((-1, 0))
        assert not map_scheme.has_position(np.array(None))
        assert not map_scheme.has_position(None)

        for free_position in map_scheme.free_positions:
            assert map_scheme.has_position(free_position)

        for obstacle_position in map_scheme.obstacles:
            assert map_scheme.has_position(obstacle_position)


@pytest.mark.parametrize("invalid_map_contents", [([0, 0, 0]), ([[[-1, 0], [-1, 0]], [[0, 0], [0, -1]]])])
def test_init_guards(invalid_map_contents):
    with pytest.raises(ValueError) as e:
        invalid_map_scheme = GridMap(invalid_map_contents)
    assert str(e.value) == "Invalid map contents supplied: must be a 2-dimensional array"
