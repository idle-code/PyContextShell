import unittest
from contextshell.session_stack.StorageLayer import StorageLayer
from contextshell.ActionNode import *


def sum_function(session: SessionLayer, target: NodePath, number: int):
    return session.get(target) + number


class DiffActionNode(ActionNode):
    def __call__(self, session: SessionLayer, target: NodePath, number: int):
        return session.get(target) - number

    @action
    def diff(self, session: SessionLayer, target: NodePath, number: int):
        return session.get(target) - number

    @action(path='my.diff')
    def my_diff(self, session: SessionLayer, target: NodePath, number: int):
        return session.get(target) - number


class ActionNodeTests(unittest.TestCase):
    def setUp(self):
        self.session = StorageLayer(Node())
        self.session.create('.foo', 3)

        self.diff_node = DiffActionNode('diff')

    def test_empty_action(self):
        self.empty_node = ActionNode('diff', callback=None)
        with self.assertRaises(NotImplementedError):
            self.empty_node(self.session, '.foo', 1, 2, 3)

    def test_from_function(self):
        sum_node = ActionNode('diff', callback=sum_function)
        six = sum_node(self.session, '.foo', 3)
        self.assertEqual(6, six)

        six = sum_node.get()(self.session, '.foo', 3)
        self.assertEqual(6, six)

    def test_from_subclass(self):
        two = self.diff_node(self.session, '.foo', 1)
        self.assertEqual(2, two)

        two = self.diff_node.get()(self.session, '.foo', 1)
        self.assertEqual(2, two)

    def test_action_decorator(self):
        self.assertEqual(NodePath('diff'), self.diff_node.diff.path)

        two = self.diff_node.diff(self.session, '.foo', 1)
        self.assertEqual(2, two)

        two = self.diff_node.diff.get()(self.session, '.foo', 1)
        self.assertEqual(2, two)

    def test_action_decorator_with_path(self):
        self.assertEqual(NodePath('my.diff'), self.diff_node.my_diff.path)

        two = self.diff_node.my_diff(self.session, '.foo', 1)
        self.assertEqual(2, two)

        two = self.diff_node.my_diff.get()(self.session, '.foo', 1)
        self.assertEqual(2, two)

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
