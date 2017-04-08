import unittest

from Node import Node
from NodePath import NodePath
from TreeRoot import TreeRoot
from actions.BasicActions import SetAction


class SetActionTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.root.append(Node(123), 'integer')
        self.root.append(Node('foobar'), 'string')
        self.root.append(Node(), 'empty')

        self.set = SetAction()

    def test_set(self):
        self.set(self.root['integer'], 321)
        self.assertEqual(321, self.root['integer'].get())
        self.set(self.root['string'], 'barfoo')
        self.assertEqual('barfoo', self.root['string'].get())

    def test_set_different_type(self):
        with self.assertRaises(TypeError):
            self.set(self.root['integer'], 'string')

    def test_set_none(self):
        # This behaviour is subject to change
        with self.assertRaises(TypeError):
            self.set(self.root['empty'], 23)

    def test_set_too_many_arguments(self):
        with self.assertRaises(TypeError):
            self.set(self.root['integer'], 1, 2, 3)


class SetActionNodeTests(unittest.TestCase):
    def setUp(self):
        self.root = TreeRoot()
        self.root.create('.integer', 123)
        self.root.create('.string', 'foobar')
        self.root.create('.empty')

    def test_set(self):
        self.root.execute('.integer', NodePath('set'), 444)
        self.assertEqual(444, self.root.get('.integer'))

        self.root.execute('.string', NodePath('set'), 'barfoo')
        self.assertEqual('barfoo', self.root.get('.string'))

    def test_set_different_type(self):
        with self.assertRaises(TypeError):
            self.root.execute('.integer', NodePath('set'), 'string')

    def test_set_none(self):
        # This behaviour is subject to change
        with self.assertRaises(TypeError):
            self.root.execute('.empty', NodePath('set'), 444)

    def test_set_any_arguments(self):
        with self.assertRaises(TypeError):
            self.root.execute('.integer', NodePath('set'), 3, 2, 1)


if __name__ == '__main__':
    unittest.main()
