import unittest
from benchmark.benchmark import Benchmark
from benchmark.test import Test
from graph.directedgraph import DirectedGraph
from entity import Entity

class TestBenchmark(unittest.TestCase):

    def setUp(self):
        self.edge_list1 = [[1,1],[1,2],[3,1]]
        self.new_map1 = DirectedGraph(self.edge_list1)
        self.entities_list1 = [Entity("A"), Entity("B"), Entity("C")]
        self.test1 = Test(self.new_map1, self.entities_list1)

        self.edge_list2 = [[1,4],[1,2],[3,1],[4,3]]
        self.new_map2 = DirectedGraph(self.edge_list2)
        self.entities_list2 = [Entity("a"), Entity("b"), Entity("c")]
        self.test2 = Test(self.new_map2, self.entities_list2) 

        self.test_list = [self.test1, self.test2]

        self.benchmark1 = Benchmark("Ciao", "Bella", [self.test1, self.test2])

        self.benchmark2 = Benchmark()

    def test_getters(self):
                
        self.assertEqual(self.benchmark1.get_name(), "Ciao")
        self.assertEqual(self.benchmark1.get_description(), "Bella")
        self.assertEqual(self.benchmark1.get_tests(), self.test_list)

        self.assertEqual(self.benchmark2.get_name(), "")
        self.assertEqual(self.benchmark2.get_description(), "")
        self.assertEqual(self.benchmark2.get_tests(), [])

    
if __name__ == '__main__':
    unittest.main()

