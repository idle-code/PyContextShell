import unittest

from contextshell.NodePath import NodePath
from contextshell.actions.BasicActions import ListAction
from contextshell.Node import Node


class ListActionTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.root.append(Node('AAA'), '@attribute')
        self.root.append(Node(), 'empty')

        self.list = ListAction()

    def test_action_names(self):
        self.assertEqual(NodePath('list'), self.list.path)
        self.assertEqual(NodePath('all'), self.list.list_all.path)
        self.assertEqual(NodePath('nodes'), self.list.list_nodes.path)
        self.assertEqual(NodePath('attributes'), self.list.list_attributes.path)

    def test_all_empty(self):
        empty_list = self.list.list_all(Node())
        self.assertListEqual([], empty_list)

    def test_all_nodes_and_attributes(self):
        root_list = self.list.list_all(self.root)
        self.assertListEqual(['@attribute', 'empty'], root_list)

    def test_nodes(self):
        root_list = self.list.list_nodes(self.root)
        self.assertListEqual(['empty'], root_list)

    def test_attributes(self):
        root_list = self.list.list_attributes(self.root)
        self.assertListEqual(['@attribute'], root_list)

    def test_default(self):
        root_list = self.list(self.root)
        self.assertListEqual(['empty'], root_list)


if __name__ == '__main__':
    unittest.main()
