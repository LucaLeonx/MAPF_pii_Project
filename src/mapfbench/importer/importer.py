"""
    Module to import maps and scenarios from external files
"""
import re

import numpy as np

from mapfbench.description import MapScheme, MapContent


def import_map(path: str) -> MapScheme:
    with open(path, "r") as file:
        map_type = file.readline()  # Skip heading 'type octile'
        map_height = _find_integer(file.readline())
        map_width = _find_integer(file.readline())
        file.readline()  # Skip 'map' heading

        map_matrix = np.empty([map_height, map_width])

        line = file.readline()
        row = 0
        while line != '':
            for col, char in enumerate(line.strip()):
                map_matrix[row, col] = _match_map_content(char)

            line = file.readline()
            row += 1

        return MapScheme(map_matrix)


def _find_integer(string: str) -> int:
    temp = re.findall(r'\d+', string)
    return list(map(int, temp))[0]


def _match_map_content(char: str) -> MapContent:
    # TODO add WATER and SWAMP
    if char == '.' or char == 'G':
        return MapContent.FREE
    elif char == 'T' or char == '@' or char == 'O':
        return MapContent.OBSTACLE
    elif char == 'S' or char == 'W':
        return MapContent.FREE
    else:
        raise ValueError(f"Invalid character {char}")
