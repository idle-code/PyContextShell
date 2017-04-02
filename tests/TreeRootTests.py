import unittest

from TreeRoot import TreeRoot
from NodePath import NodePath


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.session = TreeRoot()
        self.session.create('.foo', 1)
        self.session.create('.foo.bar', 2)
        self.session.create('.spam', "rabarbar")

    def test_get(self):
        self.assertEqual(1, self.session.get('.foo'))
        self.assertEqual(2, self.session.get('.foo.bar'))
        self.assertEqual("rabarbar", self.session.get('.spam'))

    def test_list(self):
        root_elements = self.session.list('.')
        self.assertListEqual([TreeRoot.actions_branch_name, 'foo', 'spam'], root_elements)

    def test_list_empty(self):
        self.assertListEqual([], self.session.list('.spam'))

    def test_list_nonexistent(self):
        with self.assertRaises(NameError):
            self.session.list('.rabarbar')

    def test_create(self):
        self.session.create('.baz')
        self.assertTrue(self.session.exists('.baz'))
        self.assertIsNone(self.session.get('.baz'))

    def test_create_value(self):
        self.session.create('.baz', 123)
        self.assertTrue(self.session.exists('.baz'))
        self.assertEqual(123, self.session.get('.baz'))

    def test_create_existing(self):
        with self.assertRaises(NameError):
            self.session.create('.foo')

    def test_remove(self):
        self.assertTrue(self.session.exists('.foo'))
        self.session.remove('.foo')
        self.assertFalse(self.session.exists('.foo'))

    def test_remove_nonexistent(self):
        with self.assertRaises(NameError):
            self.session.remove('.unknown.path')

    def test_exists(self):
        self.assertFalse(self.session.exists('.baz'))
        self.session.create('.baz')
        self.assertTrue(self.session.exists('.baz'))


class TreeRootTests(unittest.TestCase):
    def setUp(self):
        self.tree = TreeRoot()
        self.tree.create('.foo')
        self.tree.create('.foo.bar')

    def test_find_action(self):
        get_action_from_root = TreeRoot._find_action(self.tree.root, 'get')
        self.assertIsNotNone(get_action_from_root)

    def test_find_action_multilevel(self):
        get_action_from_foo = TreeRoot._find_action(self.tree.root['foo'], 'get')
        self.assertIsNotNone(get_action_from_foo)

        get_action_from_bar = TreeRoot._find_action(self.tree.root['foo']['bar'], 'get')
        self.assertIs(get_action_from_foo, get_action_from_bar)

    def test_find_action_from_actions(self):
        get_action_from_actions = TreeRoot._find_action(self.tree.root[TreeRoot.actions_branch_name], 'get')
        self.assertIsNotNone(get_action_from_actions)

    def test_find_unknown_action(self):
        unknown_action = TreeRoot._find_action(self.tree.root, 'unknown')
        self.assertIsNone(unknown_action)

    def test_resolve_relative(self):
        bar_path = NodePath('bar')
        bar_node = TreeRoot._resolve(self.tree.root, bar_path)
        self.assertIsNone(bar_node)
        bar_node = TreeRoot._resolve(self.tree.root['foo'], bar_path)
        self.assertIs(self.tree.root['foo']['bar'], bar_node)

    def test_resolve_absolute(self):
        bar_path = NodePath('.foo.bar')
        bar_node = TreeRoot._resolve(self.tree.root, bar_path)
        self.assertIs(self.tree.root['foo']['bar'], bar_node)
        bar_node = TreeRoot._resolve(self.tree.root['foo'], bar_path)
        self.assertIs(self.tree.root['foo']['bar'], bar_node)

    def test_resolve_nonexistent(self):
        unknown_path = NodePath('.unknown.path')
        self.assertIsNone(TreeRoot._resolve(self.tree.root, unknown_path))
        unknown_path.is_absolute = False
        self.assertIsNone(TreeRoot._resolve(self.tree.root, unknown_path))


if __name__ == '__main__':
    unittest.main()
