import unittest
from unittest.mock import MagicMock
from contextshell.NodePath import NodePath
from contextshell.actions.BasicActions import CreateAction


class CreateActionTests(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.create = CreateAction()
        self.session.exists = MagicMock(return_value=False)

    def test_action_name(self):
        self.assertEqual(NodePath('create'), self.create.path)

    def test_default_value(self):
        self.create(self.session, '.', 'default')
        self.session.create.assert_called_with(NodePath('.default'), None)

    def test_with_value(self):
        self.create(self.session, '.foo', 'value', 258)
        self.session.create.assert_called_with(NodePath('.foo.value'), 258)

    def test_existing(self):
        self.session.exists.return_value = True
        with self.assertRaises(NameError):
            self.create(self.session, '.foo', 'default')
        with self.assertRaises(NameError):
            self.create(self.session, '.foo', 'value', 123)


if __name__ == '__main__':
    unittest.main()
