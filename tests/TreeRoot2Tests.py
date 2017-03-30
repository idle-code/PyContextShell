import unittest

from CommandInterpreter import CommandInterpreter
from TreeRoot2 import TreeRoot
from NodePath import NodePath
from Node2 import *


class TreeRootViewTests(unittest.TestCase):
    def setUp(self):
        self.view = TreeRoot()

    def tearDown(self):
        for f in self.view.list('.'):
            self.view.remove(f)

    def test_get(self):
        self.assertEqual(1, self.view.get('.foo'))
        self.assertEqual(2, self.view.get('.foo.bar'))
        self.assertEqual("rabarbar", self.view.get('.spam'))

    def test_create(self):
        self.view.create('.foo')
        self.assertTrue(self.view.exists('.foo'))
        self.assertIsNone(self.view.get('.foo'))

    def test_create_value(self):
        self.view.create('.bar', 123)
        self.assertTrue(self.view.exists('.bar'))
        self.assertEqual(123, self.view.get('.bar'))

    def test_create_existing(self):
        self.view.create('.foo')
        with self.assertRaises(NameError):
            self.view.create('.foo')

    def test_remove(self):
        self.view.create('.foo')
        self.assertTrue(self.view.exists('.foo'))
        self.view.remove('.foo')
        self.assertFalse(self.view.exists('.foo'))

    def test_remove_nonexistent(self):
        with self.assertRaises(NameError):
            self.view.remove('.unknown.path')

    def test_exists(self):
        self.assertFalse(self.view.exists('.foo'))
        self.view.create('.foo')
        self.assertTrue(self.view.exists('.foo'))


@unittest.skip("CommandInterpreter might supersede this")
class TreeRootTests(unittest.TestCase):
    def setUp(self):
        self.root = TreeRoot()

    def test_basic_methods_are_present(self):
        action_path = NodePath(CommandInterpreter.actions_branch_name)
        self.assertTrue(self.root.exists(NodePath.join(action_path, 'get')))
        self.assertTrue(self.root.exists(NodePath.join(action_path, 'set')))
        self.assertTrue(self.root.exists(NodePath.join(action_path, 'list')))
        self.assertTrue(self.root.exists(NodePath.join(action_path, 'exists')))
        self.assertTrue(self.root.exists(NodePath.join(action_path, 'create')))
        self.assertTrue(self.root.exists(NodePath.join(action_path, 'remove')))


@unittest.skip("Not ready yet")
class VirtualAttributeTests(unittest.TestCase):
    def setUp(self):
        self.root = TreeRoot()
        self.root.append('foo', Node(132))

    def test_name(self):
        self.assertTrue(self.root['foo'].contains('@name'))
        foo_name = self.root['foo']['@name'].get()
        self.assertEqual('foo', foo_name)

    def test_path(self):
        self.assertTrue(self.root['foo'].contains('@path'))
        foo_path = self.root['foo']['@path'].get()
        self.assertEqual(NodePath('.foo'), foo_path)


if __name__ == '__main__':
    unittest.main()
