import unittest
from unittest.mock import MagicMock
from contextshell.NodePath import NodePath
from contextshell.actions.BasicActions import SetAction


class SetActionTests(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.session.get = MagicMock()
        self.session.set = MagicMock()

        self.action = SetAction()

    def test_action_name(self):
        self.assertEqual(NodePath('set'), self.action.path)

    def test_normal_usage(self):
        self.session.get.return_value = 123
        self.action(self.session, 'integer', 321)
        self.session.set.assert_called_once_with('integer', 321)

        self.session.get.return_value = 'foobar'
        self.session.set.reset_mock()
        self.action(self.session, 'string', 'barfoo')
        self.session.set.assert_called_once_with('string', 'barfoo')

    def test_different_type(self):
        self.session.get.return_value = 123
        with self.assertRaises(TypeError):
            self.action(self.session, 'integer', 'string')

    def test_set_none_type(self):
        # This behaviour is subject to change
        self.session.get.return_value = None
        with self.assertRaises(TypeError):
            self.action(self.session, 'empty', 23)


if __name__ == '__main__':
    unittest.main()
