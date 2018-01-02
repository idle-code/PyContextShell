import unittest

from contextshell.Node import Node
from contextshell.Shell import *
from contextshell.session_stack.SessionManager import SessionManager


class ShellTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        manager = SessionManager(self.root)

        self.shell = Shell(manager.create_session())

    def test_create_empty(self):
        self.shell.execute("create foo")
        foo_value = self.shell.execute(".foo: get")
        self.assertIsNone(foo_value)

    def test_create_string(self):
        self.shell.execute("create foo rabarbar")
        foo_value = self.shell.execute(".foo: get")
        self.assertEqual('rabarbar', foo_value)

    def test_set_string(self):
        self.test_create_string()
        self.shell.execute(".foo: set spam")
        foo_value = self.shell.execute(".foo: get")
        self.assertEqual('spam', foo_value)


class ShellCompletionTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        manager = SessionManager(self.root)

        self.shell = Shell(manager.create_session())

    def completion_on(self, command: str, cursor_position: str=None):
        pass

    @unittest.skip("Enable when shell completion will be desirable")
    def test_action_list(self):
        available_actions = self.completion_on("")
        expected_actions = [
            'get',
            'set',
            'list',
            'exists',
            'create',
            'remove']
        expected_actions = map(
            lambda n: NodePath([TreeRoot.actions_branch_name, n], absolute=True),
            expected_actions)
        self.assertListEqual(expected_actions, available_actions)

    @unittest.skip("Enable when shell completion will be desirable")
    def test_partial_action_completion(self):
        available_actions = self.completion_on("l")
        expected_actions = ['list']
        expected_actions = map(
            lambda n: NodePath([TreeRoot.actions_branch_name, n], absolute=True),
            expected_actions)
        self.assertListEqual(expected_actions, available_actions)

if __name__ == '__main__':
    unittest.main()
