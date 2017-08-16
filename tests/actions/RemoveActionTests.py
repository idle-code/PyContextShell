import unittest
from unittest.mock import MagicMock
from contextshell.NodePath import NodePath
from contextshell.actions.BasicActions import RemoveAction


class RemoveActionTests(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.session.exists = MagicMock()
        self.session.remove = MagicMock()

        self.remove = RemoveAction()

    def test_action_name(self):
        self.assertEqual(NodePath('remove'), self.remove.path)

    def test_existing(self):
        self.session.exists.return_value = True
        self.remove(self.session, '.', 'existing')
        self.session.exists.assert_called_once_with(NodePath('.existing'))
        self.session.remove.assert_called_once_with(NodePath('.existing'))

    def test_nonexistent(self):
        self.session.exists.return_value = False
        with self.assertRaises(NameError):
            self.remove(self.session, '.', 'unknown')


if __name__ == '__main__':
    unittest.main()
