import numpy as np
import pytest
import pathlib

from mapfbench.description import MapScheme
from mapfbench.importer import importer

root_path = pathlib.Path().absolute() / 'importer'


class TestImporter(object):
    # TODO additional testing and error guards
    @pytest.mark.parametrize('path, expected_map', [(
            'map_files/simple.map', MapScheme([[-1, -1, -1, -1, -1, -1],
                                               [-1, 0, 0, 0, 0, -1],
                                               [-1, 0, 0, 0, 0, -1],
                                               [-1, 0, 0, 0, 0, -1],
                                               [-1, 0, 0, 0, 0, -1],
                                               [-1, 0, 0, 0, 0, -1],
                                               [-1, -1, 0, 0, -1, -1],
                                               [-1, -1, -1, -1, -1, -1]])
    )])
    def test_map_import(self, path, expected_map):
        map_scheme = importer.import_map(root_path / path)
        assert map_scheme.width == expected_map.width
        assert map_scheme.height == expected_map.height
        assert np.array_equal(map_scheme.free_positions, expected_map.free_positions)
        assert np.array_equal(map_scheme.obstacles, expected_map.obstacles)

    def test_scenarios_import(self):
        scenarios = importer.import_scenarios(root_path / 'map_files' / 'arena.map.scen')
        assert len(scenarios) == 13

        for scenario in scenarios:
            assert scenario.map.width == 49
            assert scenario.map.height == 49
            assert scenario.map.obstacles.shape[0] == 347
            assert scenario.map.obstacles.shape[0] + scenario.map.free_positions.shape[0] == scenario.map.width * scenario.map.height

        first_scenario = scenarios[0]
        assert first_scenario.agents_num == 10
        assert first_scenario.agent_ids == list(range(1, first_scenario.agents_num + 1))
        assert first_scenario.agents[2].id == 3
        assert np.array_equal(first_scenario.agents[2].start_position, np.array([31, 23]))
        assert np.array_equal(first_scenario.agents[2].objective_position, np.array([33, 23]))
