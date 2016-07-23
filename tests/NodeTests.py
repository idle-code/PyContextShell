import unittest

from Node import *

class NodeTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()

    def test_constructor(self):
        intnode = Node(123)
        strnode = Node("spam")
        nonenode = Node()

    def test_get(self):
        intnode = Node(123)
        self.assertEqual(123, intnode.get())

        strnode = Node("spam")
        self.assertEqual("spam", strnode.get())

        nonenode = Node()
        self.assertEqual(None, nonenode.get())

    def test_set(self):
        intnode = Node(123)
        self.assertEqual(123, intnode.get())
        intnode.set(321)
        self.assertEqual(321, intnode.get())

if __name__ == '__main__':
    unittest.main()

