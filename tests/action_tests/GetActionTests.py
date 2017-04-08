import unittest

from Node import Node
from NodePath import NodePath
from actions.BasicActions import GetAction


class GetActionTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.root.append(Node(123), 'integer')
        self.root.append(Node('foobar'), 'string')
        self.root.append(Node(), 'empty')

        self.get = GetAction()

    def test_action_name(self):
        self.assertEqual(NodePath('get'), self.get.path)

    def test_normal_usage(self):
        self.assertEqual(123, self.get(self.root['integer']))
        self.assertEqual('foobar', self.get(self.root['string']))
        self.assertEqual(None, self.get(self.root['empty']))

    def test_surplus_arguments(self):
        with self.assertRaises(TypeError):
            self.get(self.root['empty'], 1 ,2 ,3)


if __name__ == '__main__':
    unittest.main()
