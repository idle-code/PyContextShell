import unittest

from IntNode import *
from Node import *


class IntNodeTests(unittest.TestCase):
    def setUp(self):
        self.node = IntNode(123)

    def test_constructor(self):
        intnode = IntNode(123)
        self.assertEqual(123, intnode.value)

        intnode = IntNode()
        self.assertEqual(0, intnode.value)

        with self.assertRaises(TypeError):
            intnode = IntNode('test')

    def test_set(self):
        self.assertEqual(123, self.node.value)
        self.node.set(self.node, 321)
        self.assertEqual(321, self.node.value)

        with self.assertRaises(TypeError):
            self.node.set(self.node, 'test')

    def test_set_min_limit(self):
        self.assertEqual(123, self.node.value)
        self.node.append_node('@minimum', Node(100))
        self.assertEqual(123, self.node.value)

        with self.assertRaises(ValueError):
            self.node.set(self.node, 99)

        self.assertEqual(123, self.node.value)

        self.node.set(self.node, 201)
        self.assertEqual(201, self.node.value)

    def test_set_max_limit(self):
        self.assertEqual(123, self.node.value)
        self.node.append_node('@maximum', Node(200))
        self.assertEqual(123, self.node.value)

        with self.assertRaises(ValueError):
            self.node.set(self.node, 201)

        self.assertEqual(123, self.node.value)

        self.node.set(self.node, 99)
        self.assertEqual(99, self.node.value)

    # TODO: test_set_max/min when value is above/below created limit

if __name__ == '__main__':
    unittest.main()
