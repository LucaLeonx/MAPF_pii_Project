import json
from json import JSONEncoder

from benchmark.benchmarkdescription import BenchmarkDescription
from benchmark.testdescription import TestDescription
from entity.agent_description import AgentDescription
from entity.entity_description import EntityDescription
from graph.edge import Edge
from graph.graph import Graph
from graph.node import Node
"""
To be improved later

class NodeEncoder(JSONEncoder):
    def default(self, node):
        return {"index": node.get_index()}


class EdgeEncoder(JSONEncoder):
    def default(self, edge):
        return {"start_node": json.dumps(edge.get_start_node(), cls=NodeEncoder),
                "end_node": json.dumps(edge.get_end_node(), cls=NodeEncoder),
                "weight": edge.get_weight()
                }


class GraphEncoder(JSONEncoder):
    def default(self, graph):
        return {"edges": json.dumps(graph.get_edges(), cls=EdgeEncoder)}


class EntityDescriptionEncoder(JSONEncoder):
    def default(self, entity):
        serialization = {
            "type": entity.__class__.__name__,
            "name": entity.get_name()}

        if entity.has_start_position():
            serialization["start_position"] = json.dumps(entity.get_start_position().get(), cls=NodeEncoder)

        return serialization


class AgentDescriptionEncoder(EntityDescriptionEncoder):
    def default(self, agent):
        serialization = super().default(agent)
        serialization["objective_name"] = agent.get_objective_name()

        return serialization


class ObstacleDescriptionEncoder(EntityDescriptionEncoder):
    pass


class ObjectiveDescriptionEncoder(EntityDescriptionEncoder):
    pass


class TestDescriptionEncoder(EntityDescriptionEncoder):
    def default(self, test):
        return {"name": test.get_name(),
                "map": json.dumps(test.get_map(), cls=GraphEncoder),
                "agents": json.dumps(test.get_agents(), cls=AgentDescriptionEncoder),
                "objectives": json.dumps(test.get_objectives(), cls=ObjectiveDescriptionEncoder),
                "obstacles": json.dumps(test.get_entities(), cls=ObstacleDescriptionEncoder)
                }


class BenchmarkDescriptionEncoder(EntityDescriptionEncoder):
    def default(self, benchmark):
        return {"name": benchmark.get_name(),
                "description": benchmark.get_description(),
                "tests": json.dumps(benchmark.get_tests(), cls=TestDescriptionEncoder)
                }
"""