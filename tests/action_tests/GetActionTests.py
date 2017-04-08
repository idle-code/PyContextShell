import unittest

from Node import Node
from NodePath import NodePath
from TreeRoot import TreeRoot
from actions.BasicActions import GetAction


class GetActionTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.root.append(Node(123), 'integer')
        self.root.append(Node('foobar'), 'string')
        self.root.append(Node(), 'empty')

        self.get = GetAction()

    def test_get(self):
        self.assertEqual(123, self.get(self.root['integer']))
        self.assertEqual('foobar', self.get(self.root['string']))
        self.assertEqual(None, self.get(self.root['empty']))

    def test_get_any_arguments(self):
        with self.assertRaises(TypeError):
            self.get(self.root['empty'], 1 ,2 ,3)


class GetActionNodeTests(unittest.TestCase):
    def setUp(self):
        self.root = TreeRoot()
        self.root.create('.integer', 123)
        self.root.create('.string', 'foobar')
        self.root.create('.empty')

    def test_get(self):
        integer = self.root.execute('.integer', NodePath('get'))
        self.assertEqual(123, integer)

        string = self.root.execute('.string', NodePath('get'))
        self.assertEqual('foobar', string)

        empty = self.root.execute('.empty', NodePath('get'))
        self.assertEqual(None, empty)

    def test_get_any_arguments(self):
        with self.assertRaises(TypeError):
            self.root.execute('.', NodePath('get'), 3, 2, 1)


if __name__ == '__main__':
    unittest.main()
