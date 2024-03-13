import unittest
from graph import directedgraph as dg

class TestDirectedGraph(unittest.TestCase):

    def setUp(self):
        self.edge_list = [[0,1], [1,2], [1,3], [3,2], [3,4], [4,3]]
        self.graph1 = dg.DirectedGraph(self.edge_list)
        self.empty_graph = dg.DirectedGraph([])
    
    def test_check_present_nodes(self):
        for i in range(5):
            with self.subTest(i=i): 
                self.assertTrue(self.graph1.is_node_present(i))

        for j in range(6,11):
            with self.subTest(j=j):
                self.assertFalse(self.graph1.is_node_present(j))

        for k in range(5):
            with self.subTest(k=k):
                self.assertFalse(self.empty_graph.is_node_present(k))


    def test_check_edges(self):
        
        # Check that all inserted edges are present
        for source,target in self.edge_list:
            with self.subTest(source=source, target=target):
                self.assertTrue(self.graph1.is_edge_present(source, target))
        
        # Check graph is directed
        reversed_edges = [[1,0],[2,1],[3,1],[2,3]]
        
        for source,target in reversed_edges:
            with self.subTest(source=source, target=target):
                self.assertFalse(self.graph1.is_edge_present(source,target))

        # Check empty graph doesn't have vertices
        for source,target in self.edge_list + [(1,0), (0,0), (1,2)]:
            with self.subTest(source=source, target=target):
                self.assertFalse(self.empty_graph.is_edge_present(source,target))

    def test_check_adjacent(self):
        self.assertEqual(self.graph1.get_adjacent_nodes(0), [1])
        self.assertEqual(self.graph1.get_adjacent_nodes(1), [2,3])
        self.assertEqual(self.graph1.get_adjacent_nodes(2), [])
        self.assertEqual(self.graph1.get_adjacent_nodes(3), [2,4])
        self.assertEqual(self.graph1.get_adjacent_nodes(4), [3])
        self.assertEqual(self.graph1.get_adjacent_nodes(5), [])

        self.assertEqual(self.empty_graph.get_adjacent_nodes(2), [])


if __name__ == '__main__':
    unittest.main()

