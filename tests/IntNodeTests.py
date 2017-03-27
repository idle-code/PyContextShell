import unittest

from IntNode import *
from Node2 import Node


class IntNodeTests(unittest.TestCase):
    def setUp(self):
        self.node = IntNode(123)

    def test_constructor(self):
        intnode = IntNode(123)
        self.assertEqual(123, intnode.get())

        intnode = IntNode()
        self.assertEqual(0, intnode.get())

        with self.assertRaises(TypeError):
            intnode = IntNode('test')

    def test_set(self):
        self.assertEqual(123, self.node.get())
        self.node.set(321)
        self.assertEqual(321, self.node.get())

        with self.assertRaises(TypeError):
            self.node.set(self.node, 'test')

    @unittest.skip
    def test_set_min_limit(self):
        self.assertEqual(123, self.node.get())
        self.node.append('@minimum', Node(100))
        self.assertEqual(123, self.node.get())

        with self.assertRaises(ValueError):
            self.node.set(99)

        self.assertEqual(123, self.node.get())

        self.node.set(201)
        self.assertEqual(201, self.node.get())

    @unittest.skip
    def test_set_max_limit(self):
        self.assertEqual(123, self.node.get())
        self.node.append('@maximum', Node(200))
        self.assertEqual(123, self.node.get())

        with self.assertRaises(ValueError):
            self.node.set(201)

        self.assertEqual(123, self.node.get())

        self.node.set(99)
        self.assertEqual(99, self.node.get())

    # TODO: test_set_max/min when value is above/below created limit

if __name__ == '__main__':
    unittest.main()
