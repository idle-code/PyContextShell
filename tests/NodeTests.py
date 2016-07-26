from Node import *

import unittest

class NodeTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()

    def test_constructor(self):
        intnode = Node(123)
        strnode = Node("spam")
        nonenode = Node()

    def test_value(self):
        intnode = Node(123)
        self.assertEqual(123, intnode.value)

        strnode = Node("spam")
        self.assertEqual("spam", strnode.value)

        nonenode = Node()
        self.assertEqual(None, nonenode.value)

    def test_set(self):
        intnode = Node(123)
        self.assertEqual(123, intnode.value)
        intnode.value = 321
        self.assertEqual(321, intnode.value)

if __name__ == '__main__':
    unittest.main()

