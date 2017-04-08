import unittest

from Node import Node
from NodePath import NodePath
from actions.BasicActions import SetAction


class SetActionTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.root.append(Node(123), 'integer')
        self.root.append(Node('foobar'), 'string')
        self.root.append(Node(), 'empty')

        self.set = SetAction()

    def test_action_name(self):
        self.assertEqual(NodePath('set'), self.set.path)

    def test_normal_usage(self):
        self.set(self.root['integer'], 321)
        self.assertEqual(321, self.root['integer'].get())
        self.set(self.root['string'], 'barfoo')
        self.assertEqual('barfoo', self.root['string'].get())

    def test_different_type(self):
        with self.assertRaises(TypeError):
            self.set(self.root['integer'], 'string')

    def test_set_none(self):
        # This behaviour is subject to change
        with self.assertRaises(TypeError):
            self.set(self.root['empty'], 23)

    def test_no_arguments(self):
        with self.assertRaises(TypeError):
            self.set(self.root['integer'])

    def test_too_many_arguments(self):
        with self.assertRaises(TypeError):
            self.set(self.root['integer'], 1, 2, 3)


if __name__ == '__main__':
    unittest.main()
