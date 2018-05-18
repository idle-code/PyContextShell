from contextshell.ActionFinder import ActionFinder
from contextshell.NodePath import NodePath

import unittest
from unittest.mock import MagicMock, call


class MakeActionPathTests(unittest.TestCase):
    def test_action_path_include_attribute_directory(self):
        finder = ActionFinder(MagicMock())
        action = NodePath('spam')

        action_path = finder.make_action_path(NodePath('foo.bar'), action)

        self.assertIn(ActionFinder.actions_branch_name, action_path)


class FindActionTests(unittest.TestCase):
    def test_action_lookup_order(self):
        # FIXME: this bottom-top lookup doesn't make sense
        tree = MagicMock()
        tree.exists.return_value = False
        finder = ActionFinder(tree)
        action = NodePath('nonexistent')

        finder.find_action(NodePath('.foo.bar'), action)

        expected_exists_calls = [
            call(finder.make_action_path(NodePath('.foo.bar'), action)),
            call(finder.make_action_path(NodePath('.foo'), action)),
            call(finder.make_action_path(NodePath('.'), action))
        ]
        self.assertEqual(tree.exists.mock_calls, expected_exists_calls)

    def test_action_doesnt_exists(self):
        tree = MagicMock()
        tree.exists.return_value = False
        finder = ActionFinder(tree)

        found_action = finder.find_action(NodePath('.'), NodePath('nonexistent'))

        self.assertIsNone(found_action)

    def test_action_exists(self):
        tree = MagicMock()
        tree.exists.return_value = True
        tree.get.return_value = 'action_implementation'
        finder = ActionFinder(tree)

        found_action = finder.find_action(NodePath('.'), NodePath('action'))

        self.assertIs(found_action, tree.get.return_value)


class InstallTests(unittest.TestCase):
    def test_install(self):
        tree = MagicMock()
        finder = ActionFinder(tree)
        target = NodePath('.')
        action_name = NodePath('action')
        action = lambda *args: None

        finder.install_action(target, action_name, action)

        tree.create.assert_called_with(finder.make_action_path(target, action_name), action)
