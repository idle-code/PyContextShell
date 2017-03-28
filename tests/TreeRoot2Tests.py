import unittest

from CommandInterpreter import CommandInterpreter
from TreeRoot2 import TreeRoot


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

    def test_name_attribute(self):
        self.root.create('foo')


if __name__ == '__main__':
    unittest.main()
