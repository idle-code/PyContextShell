from contextshell.ActionFinder import ActionFinder
from contextshell.NodePath import NodePath

import unittest
from unittest.mock import MagicMock, call


class FindActionTests(unittest.TestCase):
    def test_action_lookup_order(self):
        tree = MagicMock()
        tree.exists.return_value = False
        finder = ActionFinder(tree)
        target = NodePath('.foo.bar.spam')
        action = NodePath('nonexistent')

        finder.find_action(target, action)

        expected_exists_calls = [
            call(finder.make_action_path(NodePath('.foo.bar.spam'), action)),
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
