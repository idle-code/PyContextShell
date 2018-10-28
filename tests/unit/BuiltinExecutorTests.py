import unittest

from contextshell.action import BuiltinExecutor
from contextshell.path import NodePath
from tests.unit.fakes import FakeAction


class RegisterAction(unittest.TestCase):
    def test_no_action(self):
        executor = BuiltinExecutor()

        with self.assertRaises(ValueError):
            executor.register_builtin_action(None)

    def test_normal(self):
        executor = BuiltinExecutor()
        action = FakeAction()

        executor.register_builtin_action(action)

        self.assertIsNotNone(executor.builtin_actions.get(action.name))

    def test_duplicate(self):
        executor = BuiltinExecutor()
        action = FakeAction()
        executor.register_builtin_action(action)

        with self.assertRaises(ValueError):
            executor.register_builtin_action(action)


class ListActions(unittest.TestCase):
    def test_no_actions(self):
        executor = BuiltinExecutor()

        registered_actions = executor.list_actions_action(NodePath('.'))

        self.assertListEqual([NodePath('list.actions')], registered_actions)

    def test_single_action(self):
        executor = BuiltinExecutor()
        action = FakeAction()
        executor.register_builtin_action(action)

        registered_actions = executor.list_actions_action(NodePath('.'))

        self.assertIn(action.name, registered_actions)


class FindAction(unittest.TestCase):
    def test_nonexistent_action(self):
        executor = BuiltinExecutor()
        target = NodePath('.')

        found_action = executor.find_action(target, NodePath('unknown'))

        self.assertIsNone(found_action)

    def test_existing_action(self):
        executor = BuiltinExecutor()
        action = FakeAction()
        executor.register_builtin_action(action)
        target = NodePath('.')

        found_action = executor.find_action(target, action.name)

        self.assertIs(found_action, action)
