import importlib

from description.benchmarkdescription import BenchmarkDescription, TestDescription
from description.entity_description import AgentDescription, ObjectiveDescription, ObstacleDescription
from description.map.graph import GridGraph, UndirectedGraph, Graph, Edge, Node
from exceptions import InvalidElementException
from result.testrun import TestRun, BenchmarkRun


def extract_benchmark(dictionary):
    name = dictionary["name"]
    test_list = []

    for test_dict in dictionary["tests"]:
        test_list.append(extract_test(test_dict))

    test_occurrences = dict([(test, dictionary["test_occurrences"][test.name]) for test in test_list])
    return BenchmarkDescription(name, test_occurrences)


def extract_benchmark_run(dictionary):
    benchmark_description = extract_benchmark(dictionary)
    test_names = [test.name for test in benchmark_description.tests]
    results = dict([(name, []) for name in test_names])

    sorted_tests = sorted(dictionary["results"], key=lambda x: x["iteration"])
    for test in sorted_tests:
        test_description = [description for description in benchmark_description.tests if description.name == test["name"]]
        action_list = []

        for action in test["action_list"]:
            action_list.append(extract_action(action))

        results[test["name"]].append(TestRun(test_description, action_list, test["solved"]))

    return BenchmarkRun(benchmark_description, results)


def extract_test(dictionary) -> TestDescription:
    name = dictionary["name"]
    graph = extract_graph(dictionary["graph"])
    entities = extract_entity_list(dictionary["entities"])

    return TestDescription(name, graph, entities)


def extract_graph(dictionary):
    match dictionary["type"]:
        case "DirectedGraph":
            graph = Graph.from_dict(dictionary["graph"])
        case "UndirectedGraph":
            graph = UndirectedGraph(dictionary["graph"]["edges"])
        case "GridGraph":
            graph = GridGraph(dictionary["rows"], dictionary["cols"])
        case _:
            raise InvalidElementException(f"Error in graph representation in dictionary")

    return graph


def extract_edge(tokens: list[str]):
    string = ''.join(tokens)
    elements = string.replace('|', ',').split('|')
    return Edge(extract_node(elements[0]), extract_node(elements[1]), int(elements[2]))


def extract_node(string):
    string = string.strip()
    if string[0] == '(':
        coordinates = string[1:-1].split(',')
        return Node(int(coordinates[0]), int(coordinates[1]))
    else:
        return Node(int(string))


def extract_entity_list(dictionary):
    if "map" in dictionary:
        return dictionary["map"].entities
    else:
        entity_list = []
        for agent in dictionary["agents"]:
            info = extract_entity_info(agent)
            entity_list.append(AgentDescription(info["name"], info["objective_name"], info["start_position"]))
        for objective in dictionary["objectives"]:
            info = extract_entity_info(objective)
            entity_list.append(ObjectiveDescription(info["name"], info["start_position"]))
        for obstacle in dictionary["obstacles"]:
            info = extract_entity_info(obstacle)
            entity_list.append(ObstacleDescription(info["name"], info["start_position"]))


def extract_entity_info(dictionary):
    name = dictionary["name"]
    start_position = None
    objective_name = None

    if "start_position" in dictionary:
        start_position = extract_node(dictionary["start_position"])

    if "objective_name" in dictionary:
        objective_name = dictionary["objective_name"]

    return {"name": name, "start_position": start_position, "objective_name": objective_name}


def extract_action(dictionary):
    start_position = None
    end_position = None
    if "start_position" in dictionary:
        start_position = extract_node(dictionary["start_position"])
    if "end_position" in dictionary:
        end_position = extract_node(dictionary["end_position"])

    module = importlib.import_module('src.result.action')
    action_class = getattr(module, dictionary["type"])
    return action_class(dictionary.get("timestep"), start_position, end_position, dictionary.get("description", ""))
