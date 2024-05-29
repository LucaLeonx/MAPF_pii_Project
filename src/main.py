#!/usr/bin/python3
from result.testrun import TestRun
from metrics.testMetrics import TestMetrics

# Main file of MAPF Benchmark

def main():
    print("Hello, MAPF Benchmark!")
    metrics = TestMetrics(test_run())
    metrics.bruteForce()

def test_run():
    return TestRun.from_dict({'test_description':
                                  {'name': 'Test1',
                                   'graph': {'type': 'Graph',
                                             'edges': [
                                                 {'start_node': {'index': 1}, 'end_node': {'index': 2}, 'weight': 1},
                                                 {'start_node': {'index': 3}, 'end_node': {'index': 4}, 'weight': 1},
                                                 {'start_node': {'index': 2}, 'end_node': {'index': 3}, 'weight': 1},
                                                 {'start_node': {'index': 3}, 'end_node': {'index': 2}, 'weight': 1},
                                                 {'start_node': {'index': 1}, 'end_node': {'index': 3}, 'weight': 1}]},
                                   'entities': [{'type': 'ObjectiveDescription', 'name': 'T1'},
                                                {'type': 'ObjectiveDescription', 'name': 'T2'},
                                                {'type': 'ObjectiveDescription', 'name': 'T3'},
                                                {'type': 'AgentDescription', 'name': 'A1',
                                                 'start_position': {'index': 1}, 'objective': 'T1'},
                                                {'type': 'AgentDescription', 'name': 'A2',
                                                 'start_position': {'index': 2}, 'objective': 'T2'},
                                                {'type': 'AgentDescription', 'name': 'A3',
                                                 'start_position': {'index': 3}, 'objective': 'T3'},
                                                {'type': 'ObstacleDescription', 'name': 'O1'}]},
                              'action_list': [
                                  {'type': 'AppearAction', 'timestep': 0, 'subject': 'A1', 'end_position': {'index': 1},
                                   'description': 'Appear'},
                                  {'type': 'AppearAction', 'timestep': 0, 'subject': 'A2', 'end_position': {'index': 2},
                                   'description': 'Appear'},
                                  {'type': 'AppearAction', 'timestep': 0, 'subject': 'A3', 'end_position': {'index': 3},'description': 'Appear'},
                                  {'type': 'MoveAction', 'timestep': 1, 'subject': 'A1', 'start_position': {'index': 1},'end_position': {'index': 2}, 'description': 'Move'},
                                  {'type': 'MoveAction', 'timestep': 1, 'subject': 'A2', 'start_position': {'index': 2},'end_position': {'index': 1}, 'description': 'Move'},
                                  {'type': 'MoveAction', 'timestep': 1, 'subject': 'A3', 'start_position': {'index': 3},'end_position': {'index': 4}, 'description': 'Move'},
                                  {'type': 'WaitAction', 'timestep': 2, 'subject': 'A2', 'start_position': {'index': 3},'description': 'Wait'},
                                  {'type': 'DisappearAction', 'timestep': 2, 'subject': 'A1',
                                   'description': 'Disappear'},
                                  {'type': 'AppearAction', 'timestep': 3, 'subject': 'T3',
                                   'end_position': {'index': 12}, 'description': 'Appear'},
                                  {'type': 'MoveAction', 'timestep': 4, 'subject': 'T3',
                                   'start_position': {'index': 12}, 'end_position': {'index': 8},
                                   'description': 'MoveLeft'},
                                  {'type': 'MoveAction', 'timestep': 5, 'subject': 'T3', 'start_position': {'index': 8},
                                   'end_position': {'index': 13}, 'description': 'MoveUp'}],
                              'is_solved': False})

if __name__ == "__main__":
    main()
    


    