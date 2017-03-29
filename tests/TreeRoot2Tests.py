import unittest

from CommandInterpreter import CommandInterpreter
from TreeRoot2 import TreeRoot
from NodePath import NodePath
from Node2 import *


class TreeRootTests(unittest.TestCase):
    def setUp(self):
        self.root = TreeRoot()

    def test_basic_methods(self):
        actions_node = self.root.get_node(CommandInterpreter.actions_branch_name)
        self.assertIsNotNone(actions_node)

        self.assertTrue(actions_node.contains('get'))
        self.assertTrue(actions_node.contains('set'))
        self.assertTrue(actions_node.contains('list'))
        self.assertTrue(actions_node.contains('create'))
        self.assertTrue(actions_node.contains('remove'))


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
