import numpy as np
import pytest

from mapfbench.description.mapscheme import MapScheme


class TestMapScheme:

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
    def test_getters(self, map_contents, exp_width, exp_height, exp_free_positions, exp_obstacles):
        # mapscheme = MapScheme(np.array([[0, 0, 0],
        #                                [-1, 0, -1],
        #                                [0, -1, 0]]))

        map_scheme = MapScheme(np.array(map_contents))
        print(map_scheme.free_positions)
        assert map_scheme.width == exp_width
        assert map_scheme.height == exp_height

        assert np.array_equal(map_scheme.free_positions, np.array(exp_free_positions))
        assert np.array_equal(map_scheme.obstacles, np.array(exp_obstacles))

    @pytest.mark.parametrize("invalid_map_contents", [([0, 0, 0]), ([[[-1, 0], [-1, 0]], [[0, 0], [0, -1]]])])
    def test_init_guards(self, invalid_map_contents):

        with pytest.raises(ValueError) as e:
            invalid_map_scheme = MapScheme(np.array(invalid_map_contents))

        assert str(e.value) == "Invalid map contents supplied: must be a 2-dimensional array"
