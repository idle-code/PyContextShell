import unittest
from unittest.mock import MagicMock
from contextshell.NodePath import NodePath
from contextshell.actions.BasicActions import GetAction


class GetActionTests(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.session.get = MagicMock()

        self.get = GetAction()

    def test_action_name(self):
        self.assertEqual(NodePath('get'), self.get.path)

    def test_normal_usage(self):
        self.session.get.return_value=123
        self.assertEqual(123, self.get(self.session, 'integer'))
        self.session.get.assert_called_once_with('integer')

        self.session.get.reset_mock()
        self.session.get.return_value = None
        self.assertIsNone(self.get(self.session, 'empty'))
        self.session.get.assert_called_once_with('empty')


if __name__ == '__main__':
    unittest.main()
