import unittest
from unittest.mock import MagicMock
from contextshell.NodePath import NodePath
from contextshell.actions.BasicActions import ListAction


class ListActionTests(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.session.list = MagicMock(return_value=list(map(NodePath.cast, ['@attribute', 'empty'])))

        self.list = ListAction()

    def test_action_names(self):
        self.assertEqual(NodePath('list'), self.list.path)
        self.assertEqual(NodePath('all'), self.list.list_all.path)
        self.assertEqual(NodePath('nodes'), self.list.list_nodes.path)
        self.assertEqual(NodePath('attributes'), self.list.list_attributes.path)

    def _compare_output(self, actual_list, expected_list):
        expected_path_list = list(map(NodePath.cast, expected_list))
        self.assertEqual(actual_list, expected_path_list)
        for path in actual_list:
            self.assertTrue(path.is_absolute, "'{}' is not absolute".format(path))

    def test_all_empty(self):
        self.session.list.return_value = []
        self._compare_output(self.list.list_all(self.session, '.'), [])

    def test_all_nodes_and_attributes(self):
        self._compare_output(self.list.list_all(self.session, '.'), ['.@attribute', '.empty'])
        self.session.list.assert_called_once_with('.')

    def test_nodes(self):
        self._compare_output(self.list.list_nodes(self.session, '.'), ['.empty'])
        self.session.list.assert_called_once_with('.')

    def test_attributes(self):
        self._compare_output(self.list.list_attributes(self.session, '.'), ['.@attribute'])
        self.session.list.assert_called_once_with('.')

    def test_default(self):
        self.test_nodes()


if __name__ == '__main__':
    unittest.main()
