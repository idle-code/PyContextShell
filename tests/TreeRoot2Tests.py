import unittest

from TreeRoot2 import TreeRoot
from NodePath import NodePath


class TreeRootViewTests(unittest.TestCase):
    def setUp(self):
        self.view = TreeRoot()
        self.view.create('.foo', 1)
        self.view.create('.foo.bar', 2)
        self.view.create('.spam', "rabarbar")

    def test_get(self):
        self.assertEqual(1, self.view.get('.foo'))
        self.assertEqual(2, self.view.get('.foo.bar'))
        self.assertEqual("rabarbar", self.view.get('.spam'))

    def test_list(self):
        root_elements = self.view.list('.')
        self.assertListEqual([TreeRoot.actions_branch_name, 'foo', 'spam'], root_elements)

    def test_list_empty(self):
        self.assertListEqual([], self.view.list('.spam'))

    def test_list_nonexistent(self):
        with self.assertRaises(NameError):
            self.view.list('.rabarbar')

    def test_create(self):
        self.view.create('.baz')
        self.assertTrue(self.view.exists('.baz'))
        self.assertIsNone(self.view.get('.baz'))

    def test_create_value(self):
        self.view.create('.baz', 123)
        self.assertTrue(self.view.exists('.baz'))
        self.assertEqual(123, self.view.get('.baz'))

    def test_create_existing(self):
        with self.assertRaises(NameError):
            self.view.create('.foo')

    def test_remove(self):
        self.assertTrue(self.view.exists('.foo'))
        self.view.remove('.foo')
        self.assertFalse(self.view.exists('.foo'))

    def test_remove_nonexistent(self):
        with self.assertRaises(NameError):
            self.view.remove('.unknown.path')

    def test_exists(self):
        self.assertFalse(self.view.exists('.baz'))
        self.view.create('.baz')
        self.assertTrue(self.view.exists('.baz'))


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


class VirtualAttributeTests(unittest.TestCase):
    def setUp(self):
        self.view = TreeRoot()
        self.view.create('.foo', 1)
        self.view.create('.foo.bar', 2)
        self.view.create('.baz', "SPAM")

    def test_name(self):
        self.assertTrue(self.view.exists('.foo.@name'))
        self.assertEqual('foo', self.view.get('.foo.@name'))

    def test_path(self):
        self.assertTrue(self.view.exists('.foo.bar.@path'))
        self.assertEqual(NodePath('.foo.bar'), self.view.get('.foo.@path'))

    def test_index(self):
        self.assertTrue(self.view.exists('.foo.@index'))
        self.assertTrue(self.view.exists('.foo.bar.@index'))
        self.assertTrue(self.view.exists('.baz.@index'))
        root_names = self.view.list('.')
        root_indices = map(lambda name: self.view.get(NodePath.join(name, '@index')), root_names)
        root_indices = list(root_indices)
        self.assertListEqual([0, 1], root_indices)

if __name__ == '__main__':
    unittest.main()
