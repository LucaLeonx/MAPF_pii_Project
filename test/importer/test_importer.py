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
        importer.import_scenarios(root_path / 'map_files' / 'arena.map.scen')