import unittest
from benchmark.test import Test
from graph.directedgraph import DirectedGraph
from entity import Entity

class TestTestClass(unittest.TestCase):

    def setUp(self):
        self.edge_list = [[1,1],[1,2],[3,1]]
        self.new_map = DirectedGraph(self.edge_list)
        self.entities_list = [Entity("A"), Entity("B"), Entity("C")]
        self.test1 = Test(self.new_map, self.entities_list)
        self.empty_test = Test(DirectedGraph([]), [])

    def test_getters(self):                             
        for source,target in self.edge_list:
            with self.subTest(source=source, target=target):
                self.assertTrue(self.test1.get_field().is_edge_present(source,target))
        
        self.assertEqual([entity.get_label() for entity in self.test1.get_entities()], ["A", "B", "C"])

        for node in range(5):
            with self.subTest(node=node):
                self.assertFalse(self.empty_test.get_field().is_node_present(node))

        self.assertEqual(self.empty_test.get_entities(), [])



if __name__ == '__main__':
    unittest.main()

