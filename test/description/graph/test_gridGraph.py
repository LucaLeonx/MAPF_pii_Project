from description.graph import GridGraph, Edge, Node


class TestGridGraph(object):

    def test_edge_creation(self):
        assert GridGraph(1, 1).edges == []

        two_graph = set(GridGraph(2, 1).edges) == {
            Edge(Node(coords=(0, 0)), Node(coords=(0, 1))),
            Edge(Node(coords=(0, 1)), Node(coords=(0, 0)))
        }

        square_graph = GridGraph(2, 2)

        assert set(square_graph.nodes) == {Node(coords=(0, 0)),
                                           Node(coords=(0, 1)),
                                           Node(coords=(1, 0)),
                                           Node(coords=(1, 1))}

        undirected_edges = set(square_graph.undirected_edges)
        edges_to_check = {Edge(Node(coords=(0, 0)), Node(coords=(0, 1))),
                          Edge(Node(coords=(0, 1)), Node(coords=(1, 1))),
                          Edge(Node(coords=(1, 1)), Node(coords=(1, 0))),
                          Edge(Node(coords=(1, 0)), Node(coords=(0, 0)))}

        assert len(undirected_edges) == 4
        for edge in edges_to_check:
            assert edge in undirected_edges or edge.reversed() in undirected_edges

        rect_graph = GridGraph(2, 3)
        print([str(edge) for edge in rect_graph.undirected_edges])
        assert len(rect_graph.nodes) == 6
        assert len(rect_graph.undirected_edges) == 7

        for node in rect_graph.nodes:
            print(node)


