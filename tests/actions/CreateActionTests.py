import unittest

from contextshell.NodePath import NodePath
from contextshell.actions.BasicActions import CreateAction
from contextshell.Node import Node


class CreateActionTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.root.append(Node(123), 'existing')

        self.create = CreateAction()

    def test_action_name(self):
        self.assertEqual(NodePath('create'), self.create.path)

    def test_default_value(self):
        self.assertFalse(self.root.contains('default'))
        self.create(self.root, 'default')
        self.assertTrue(self.root.contains('default'))
        self.assertIsNone(self.root['default'].get())

    def test_with_value(self):
        self.assertFalse(self.root.contains('value'))
        self.create(self.root, 'value', 258)
        self.assertTrue(self.root.contains('value'))
        self.assertEqual(258, self.root['value'].get())

    def test_existing(self):
        self.assertTrue(self.root.contains('existing'))
        with self.assertRaises(NameError):
            self.create(self.root, 'existing')
        with self.assertRaises(NameError):
            self.create(self.root, 'existing', 'value')

    def test_surplus_arguments(self):
        with self.assertRaises(TypeError):
            self.create(self.root, 'surplus', 'value', 'value2')

    def test_no_arguments(self):
        with self.assertRaises(TypeError):
            self.create(self.root)

if __name__ == '__main__':
    unittest.main()
