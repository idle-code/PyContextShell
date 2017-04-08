import unittest

from Node import Node
from NodePath import NodePath
from actions.BasicActions import ExistsAction


class ExistsActionTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.root.append(Node(123), 'integer')
        self.root.append(Node('foobar'), 'string')
        self.root.append(Node(), 'empty')

        self.exists = ExistsAction()

    def test_action_name(self):
        self.assertEqual(NodePath('exists'), self.exists.path)

    def test_existing(self):
        self.assertTrue(self.exists(self.root, 'integer'))
        self.assertTrue(self.exists(self.root, 'empty'))

    def test_nonexistent(self):
        self.assertFalse(self.exists(self.root, 'unknown'))

    def test_surplus_arguments(self):
        with self.assertRaises(TypeError):
            self.exists(self.root, 'unknown', 'name')

    def test_no_argument(self):
        with self.assertRaises(TypeError):
            self.exists(self.root)


if __name__ == '__main__':
    unittest.main()
