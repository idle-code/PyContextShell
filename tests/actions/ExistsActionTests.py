import unittest
from unittest.mock import MagicMock
from contextshell.NodePath import NodePath
from contextshell.actions.BasicActions import ExistsAction


class ExistsActionTests(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.session.exists = MagicMock()

        self.exists = ExistsAction()

    def test_action_name(self):
        self.assertEqual(NodePath('exists'), self.exists.path)

    def test_existing(self):
        self.session.exists.return_value = True
        self.assertTrue(self.exists(self.session, '.', 'integer'))
        self.session.exists.assert_called_once_with(NodePath('.integer'))

    def test_nonexistent(self):
        self.session.exists.return_value = False
        self.assertFalse(self.exists(self.session, '.', 'unknown'))
        self.session.exists.assert_called_once_with(NodePath('.unknown'))


if __name__ == '__main__':
    unittest.main()
