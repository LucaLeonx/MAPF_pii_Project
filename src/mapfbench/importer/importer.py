"""
    Module to import maps and scenarios from external files
"""
import re
from pathlib import Path

import numpy as np

from mapfbench.description import MapContent, Scenario, Agent, GridMap


def import_map(path: str) -> GridMap:
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

        return GridMap(map_matrix)


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


def import_scenarios(filename: str) -> list[Scenario]:
    scenario_agents: dict[int, list[Agent]] = {}
    scenario_maps: dict[int, MapScheme] = {}
    cached_maps: dict[str, MapScheme] = {}
    with open(filename, 'r') as f:

        parent_dir = Path(filename).parent
        f.readline()  # Skip version number
        for line in f:
            # Tokens on format: bucket, map file, map-width, map-height, start-x, start-y, obj-x, obj-y
            tokens = line.split()
            bucket = int(tokens[0])
            map_file = tokens[1]
            start_x = int(tokens[4])
            start_y = int(tokens[5])
            objective_x = int(tokens[6])
            objective_y = int(tokens[7])

            if bucket not in scenario_maps:
                map_scheme = None
                if map_file in cached_maps:
                    map_scheme = cached_maps[map_file]
                else:
                    try:
                        map_scheme = import_map(parent_dir / map_file)
                        cached_maps.update({map_file: map_scheme})
                    except FileNotFoundError:
                        raise FileNotFoundError(f"File of the map {tokens[1]} not found")
                scenario_maps.update({bucket: map_scheme})
            if bucket not in scenario_agents:
                scenario_agents.update({bucket: []})

            agent = Agent(len(scenario_agents[bucket]) + 1,
                          (start_x, start_y),
                          (objective_x, objective_y))
            scenario_agents[bucket].append(agent)

    scenarios = []
    for bucket in scenario_agents.keys():
        scenario = Scenario(scenario_maps[bucket], scenario_agents[bucket], metadata={"bucket": bucket, "filename": filename})
        scenarios.append(scenario)

    return scenarios
