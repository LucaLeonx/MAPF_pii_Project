from graph.node import Node


class Edge:
    def __init__(self, start_node, end_node, weight=1):
        self._start_node = start_node
        self._end_node = end_node
        self._weight = weight

    def get_start_node(self):
        return self._start_node

    def get_end_node(self):
        return self._end_node

    def get_weight(self):
        return self._weight

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self._start_node == other.get_start_node() and
                self._end_node == other.get_end_node() and
                self._weight == other.get_weight())

    def __hash__(self):
        return hash((self._start_node, self.get_end_node(), self._weight))

    def __str__(self):
        return f"({self.get_start_node()}, {self.get_end_node()} | {self._weight})"

    def to_dict(self, use_coordinates=False):
        return {"start_node": self._start_node.to_dict(use_coordinates),
                "end_node": self._end_node.to_dict(use_coordinates),
                "weight": self._weight}

    @staticmethod
    def from_dict(dictionary, use_coordinates=False):
        return Edge(Node.from_dict(dictionary["start_node"], use_coordinates),
                    Node.from_dict(dictionary["end_node"], use_coordinates),
                    dictionary["weight"])

