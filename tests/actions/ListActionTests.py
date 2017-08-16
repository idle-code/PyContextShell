import unittest
from unittest.mock import MagicMock
from contextshell.NodePath import NodePath
from contextshell.actions.BasicActions import ListAction


class ListActionTests(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.session.list = MagicMock(return_value=['@attribute', 'empty'])

        self.list = ListAction()

    def test_action_names(self):
        self.assertEqual(NodePath('list'), self.list.path)
        self.assertEqual(NodePath('all'), self.list.list_all.path)
        self.assertEqual(NodePath('nodes'), self.list.list_nodes.path)
        self.assertEqual(NodePath('attributes'), self.list.list_attributes.path)

    def test_all_empty(self):
        self.session.list.return_value = []
        empty_list = self.list.list_all(self.session, '.')
        self.assertListEqual([], empty_list)

    def test_all_nodes_and_attributes(self):
        root_list = self.list.list_all(self.session, '.')
        self.session.list.assert_called_once_with('.')
        self.assertListEqual(['@attribute', 'empty'], root_list)

    def test_nodes(self):
        root_list = self.list.list_nodes(self.session, '.')
        self.session.list.assert_called_once_with('.')
        self.assertListEqual(['empty'], root_list)

    def test_attributes(self):
        root_list = self.list.list_attributes(self.session, '.')
        self.session.list.assert_called_once_with('.')
        self.assertListEqual(['@attribute'], root_list)

    def test_default(self):
        root_list = self.list(self.session, '.')
        self.session.list.assert_called_once_with('.')
        self.assertListEqual(['empty'], root_list)


if __name__ == '__main__':
    unittest.main()
