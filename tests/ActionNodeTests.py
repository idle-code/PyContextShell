import unittest

from ActionNode import *
from NodePath import NodePath


def sum_function(target: Node, number: int):
    return target.get() + number


class DiffActionNode(ActionNode):
    def __call__(self, target: Node, number: int):
        return target.get() - number

    @action
    def diff(self, target: Node, number: int):
        return target.get() - number

    @action(path='my.diff')
    def my_diff(self, target: Node, number: int):
        return target.get() - number


class ActionNodeTests(unittest.TestCase):
    def setUp(self):
        self.target = Node(3)

    def test_empty_action(self):
        self.empty_node = ActionNode('diff', callback=None)
        with self.assertRaises(NotImplementedError):
            self.empty_node(self.target, 1, 2, 3)

    def test_from_function(self):
        self.sum_node = ActionNode('diff', callback=sum_function)
        six = self.sum_node(self.target, 3)
        self.assertEqual(6, six)

    def test_from_subclass(self):
        self.diff_node = DiffActionNode('diff')

        two = self.diff_node(self.target, 1)
        self.assertEqual(2, two)

    def test_action_decorator(self):
        self.diff_node = DiffActionNode('diff')

        two = self.diff_node.diff(self.target, 1)
        self.assertEqual(2, two)
        self.assertEqual(NodePath('diff'), self.diff_node.diff.path)

    def test_action_decorator_with_path(self):
        self.diff_node = DiffActionNode('diff')

        two = self.diff_node.my_diff(self.target, 1)
        self.assertEqual(2, two)
        self.assertEqual(NodePath('my.diff'), self.diff_node.my_diff.path)

    def test_none_path(self):
        with self.assertRaises(ValueError):
            ActionNode(path=None, callback=lambda x: x)

    def test_absolute_path(self):
        absolute_path = NodePath('.foo.bar')
        with self.assertRaises(ValueError):
            ActionNode(path=absolute_path, callback=lambda x: x)

    def test_path(self):
        act = ActionNode(path='foo', callback=lambda x: x)
        self.assertEqual(NodePath('foo'), act.path)

    def test_path_nested(self):
        action_path = NodePath('foo.bar')
        act = ActionNode(path=action_path, callback=lambda x: x)
        self.assertEqual(NodePath('foo.bar'), act.path)


if __name__ == '__main__':
    unittest.main()
