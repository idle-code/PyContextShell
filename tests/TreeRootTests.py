import unittest

from contextshell.ActionNode import ActionNode
from contextshell.TreeRoot import TreeRoot


class TreeRootTests(unittest.TestCase):
    def setUp(self):
        self.tree = TreeRoot()
        self.session = self.tree.create_session()
        self.session.create('.foo')
        self.session.create('.foo.bar')

    # def test_find_action(self):
    #     get_action_from_root = TreeRoot._find_action(self.tree.root, 'get')
    #     self.assertIsNotNone(get_action_from_root)
    #
    # def test_find_action_multilevel(self):
    #     get_action_from_foo = TreeRoot._find_action(self.tree.root['foo'], 'get')
    #     self.assertIsNotNone(get_action_from_foo)
    #
    #     get_action_from_bar = TreeRoot._find_action(self.tree.root['foo']['bar'], 'get')
    #     self.assertIs(get_action_from_foo, get_action_from_bar)
    #
    # def test_find_action_from_actions(self):
    #     get_action_from_actions = TreeRoot._find_action(self.tree.root[TreeRoot.actions_branch_name], 'get')
    #     self.assertIsNotNone(get_action_from_actions)
    #
    # def test_find_unknown_action(self):
    #     unknown_action = TreeRoot._find_action(self.tree.root, 'unknown')
    #     self.assertIsNone(unknown_action)

    # def test_resolve_relative(self):
    #     bar_path = NodePath('bar')
    #     bar_node = TreeRoot._resolve(self.tree.root, bar_path)
    #     self.assertIsNone(bar_node)
    #     bar_node = TreeRoot._resolve(self.tree.root['foo'], bar_path)
    #     self.assertIs(self.tree.root['foo']['bar'], bar_node)
    #
    # def test_resolve_absolute(self):
    #     bar_path = NodePath('.foo.bar')
    #     bar_node = TreeRoot._resolve(self.tree.root, bar_path)
    #     self.assertIs(self.tree.root['foo']['bar'], bar_node)
    #     bar_node = TreeRoot._resolve(self.tree.root['foo'], bar_path)
    #     self.assertIs(self.tree.root['foo']['bar'], bar_node)
    #
    # def test_resolve_nonexistent(self):
    #     unknown_path = NodePath('.unknown.path')
    #     self.assertIsNone(TreeRoot._resolve(self.tree.root, unknown_path))
    #     unknown_path.is_absolute = False
    #     self.assertIsNone(TreeRoot._resolve(self.tree.root, unknown_path))

    def test_install_action_none(self):
        with self.assertRaises(ValueError):
            self.tree.install_action(None)

    def test_install_action(self):
        action = ActionNode('act', lambda x: x)
        self.tree.install_action(action)
        self.assertTrue(self.session.exists('.@actions.act'))

    def test_install_action_nested(self):
        action = ActionNode('foo.bar', lambda x: x)
        self.tree.install_action(action)
        self.assertTrue(self.session.exists('.@actions.foo.bar'))

    def test_install_action_in_path(self):
        action = ActionNode('foo.bar', lambda x: x)
        self.tree.install_action(action, 'foo')
        self.assertTrue(self.session.exists('.foo.@actions.foo.bar'))

if __name__ == '__main__':
    unittest.main()
