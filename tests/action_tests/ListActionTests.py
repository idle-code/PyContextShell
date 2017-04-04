import unittest

from Node import Node
from NodePath import NodePath
from TreeRoot import TreeRoot
from actions.BasicActions import ListAction


class ListActionTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.root.append(Node('AAA'), '@attribute')
        self.root.append(Node(), 'empty')

        self.list = ListAction()

    def test_list_all_empty(self):
        empty_list = self.list.list_all(Node())
        self.assertListEqual([], empty_list)

    def test_list_all_nodes_and_attributes(self):
        root_list = self.list.list_all(self.root)
        self.assertListEqual(['@attribute', 'empty'], root_list)

    def test_list_nodes(self):
        root_list = self.list.list_nodes(self.root)
        self.assertListEqual(['empty'], root_list)

    def test_list_attributes(self):
        root_list = self.list.list_attributes(self.root)
        self.assertListEqual(['@attribute'], root_list)

    def test_list_default(self):
        root_list = self.list(self.root)
        self.assertListEqual(['empty'], root_list)


class ListActionNodeTests(unittest.TestCase):
    def setUp(self):
        self.root = TreeRoot()
        self.root.create('.test')
        self.root.create('.test.@attribute', 'AAA')
        self.root.create('.test.empty', '')

        # Note: ListAction should be already present in TreeRoot

    def test_list_all_empty(self):
        empty_list = self.root.execute('.test.empty', NodePath('list.all'))
        self.assertListEqual([], empty_list)

    def test_list_all_nodes_and_attributes(self):
        root_list = self.root.execute('.test', NodePath('list.all'))
        self.assertListEqual(['@attribute', 'empty'], root_list)

    def test_list_nodes(self):
        root_list = self.root.execute('.test', NodePath('list.nodes'))
        self.assertListEqual(['empty'], root_list)

    def test_list_attributes(self):
        root_list = self.root.execute('.test', NodePath('list.attributes'))
        self.assertListEqual(['@attribute'], root_list)

    def test_list_default(self):
        root_list = self.root.execute('.test', NodePath('list'))
        self.assertListEqual(['empty'], root_list)


if __name__ == '__main__':
    unittest.main()
