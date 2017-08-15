import unittest

from contextshell.NodePath import NodePath
from contextshell.actions.BasicActions import RemoveAction

from contextshell.Node import Node


class RemoveActionTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.root.append(Node(123), 'existing')

        self.remove = RemoveAction()

    def test_action_name(self):
        self.assertEqual(NodePath('remove'), self.remove.path)

    def test_existing(self):
        self.assertTrue(self.root.contains('existing'))
        self.remove(self.root, 'existing')
        self.assertFalse(self.root.contains('existing'))

    def test_nonexistent(self):
        self.assertFalse(self.root.contains('unknown'))
        with self.assertRaises(NameError):
            self.remove(self.root, 'unknown')

    def test_surplus_arguments(self):
        with self.assertRaises(TypeError):
            self.remove(self.root, 'existing', 'name')

    def test_no_argument(self):
        with self.assertRaises(TypeError):
            self.remove(self.root)


if __name__ == '__main__':
    unittest.main()
