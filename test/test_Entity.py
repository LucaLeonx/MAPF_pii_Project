import unittest

from entity import Entity
from optional import Optional

class TestEntity(unittest.TestCase):

    def setUp(self):
        self.a = Entity("A", "Entity One", 1) 
        self.b = Entity("B", "Another entity", 2)
        self.c = Entity("C", "Third Entity", 1)
        self.d = Entity("D", "No position")
        self.no_info = Entity("X") # Entity with a label only

    def test_getters(self):
        self.assertEqual(self.a.get_label(), "A")
        self.assertEqual(self.a.get_description(), "Entity One")
        self.assertEqual(self.a.get_position(), Optional.of(1))
    
    def test_constructor_defaults(self):
        self.assertEqual(self.d.get_position(), Optional.of(None))

        self.assertEqual(self.no_info.get_description(), "")
        self.assertEqual(self.no_info.get_position(), Optional.of(None))

    def test_position_methods(self):
        
        self.assertFalse(self.no_info.is_position_available()) 
        self.no_info.set_position(10)
        
        self.assertTrue(self.no_info.is_position_available())
        self.no_info.disappear()
        
        self.assertFalse(self.no_info.is_position_available()) 
        
    def test_collision_detection(self):
        self.assertTrue(self.a.is_colliding_with(self.c))
        self.assertTrue(self.c.is_colliding_with(self.c))
        self.assertFalse(self.a.is_colliding_with(self.b))
        self.assertFalse(self.a.is_colliding_with(self.no_info))
        self.assertFalse(self.no_info.is_colliding_with(self.a))

    #def tearDown(self)


if __name__ == '__main__':
    unittest.main()

