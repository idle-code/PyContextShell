import unittest
from unittest.mock import MagicMock

from contextshell.Node import Node
from contextshell.NodePath import NodePath
from contextshell.Command import Command
from contextshell.CommandInterpreter import CommandInterpreter
from contextshell.ActionNode import ActionNode


class FakeTree:
    existing_paths: [NodePath]

    def __init__(self):
        self.existing_paths = []

    def exists(self, path: NodePath) -> bool:
        return path in self.existing_paths


class FakeActionFinder:
    existing_actions: [NodePath]

    def __init__(self):
        self.existing_actions = []

    def find(self, target: NodePath, action_path: NodePath):
        return action_path in self.existing_actions


class CommandInterpreterTests(unittest.TestCase):
    def CreateCommand(self, line: str) -> Command:
        from contextshell.CommandParser import CommandParser
        return CommandParser().parse(line)

    def CreateTree(self):
        return FakeTree()

    def CreateActionFinder(self):
        return FakeActionFinder()

    def CreateInterpreter(self, action_finder, session) -> CommandInterpreter:
        return CommandInterpreter(action_finder, session)

    def test_unknown_target(self):
        action_finder = self.CreateActionFinder()
        unknown_target_cmd = self.CreateCommand('.unknown_target: get')
        action_finder.existing_actions.append(unknown_target_cmd.name)
        interpreter = self.CreateInterpreter(action_finder, self.CreateTree())

        with self.assertRaises(NameError):
            interpreter.execute(unknown_target_cmd)

    def test_unknown_action(self):
        interpreter = self.CreateInterpreter(self.CreateActionFinder(), self.CreateTree())
        unknown_action_cmd = self.CreateCommand('.: unknown_action')

        with self.assertRaises(NameError):
            interpreter.execute(unknown_action_cmd)

    def test_recursive_target_evaluation(self):
        self.session.create('.foo.name', ".foo")

        get_name_cmd = Command('get')
        get_name_cmd.target = '.foo.name'

        get_cmd = Command('get')
        get_cmd.target = get_name_cmd

        # Execute:
        #   {foo.name: get}: get
        foo_val = self.interpreter.execute(get_cmd)
        self.assertEqual(foo_val, self.session.get('.foo'))

    def test_recursive_action_evaluation(self):
        self.session.create('.foo.action', "get")

        get_action_cmd = Command('get')
        get_action_cmd.target = '.foo.action'
        get_cmd = Command(get_action_cmd)
        get_cmd.target = '.foo'

        # Execute:
        #   foo: {foo.action: get}
        foo_val = self.interpreter.execute(get_cmd)
        self.assertEqual(foo_val, self.session.get('.foo'))

    def test_recursive_argument_evaluation(self):
        self.session.create('.foo.value', 123)

        get_value_cmd = Command('get')
        get_value_cmd.target = '.foo.value'

        set_cmd = Command('set')
        set_cmd.target = '.foo'
        set_cmd.arguments = [get_value_cmd]

        # Execute:
        #   foo: set {foo.value: get}
        self.interpreter.execute(set_cmd)
        self.assertEqual(123, self.session.get('.foo'))


class CommandLookupTests(unittest.TestCase):
    class ReturnAction(ActionNode):
        def __init__(self, name: str, return_value):
            super().__init__(NodePath(name))
            self.return_value = return_value

        def __call__(self, session: CrudSessionLayer, target: NodePath, *arguments):
            return self.return_value

    def setUp(self):
        root = Node()
        manager = SessionManager(root)
        self.session = manager.create_session()
        self.interpreter = CommandInterpreter(self.session)

        self.session.create('.foo', 1)
        self.session.create('.foo.bar', 2)
        self.session.install_action(CommandLookupTests.ReturnAction('num', 'ROOT'))
        self.session.install_action(CommandLookupTests.ReturnAction('num', 'FOO'), '.foo')
        self.session.install_action(CommandLookupTests.ReturnAction('num', 'BAR'), '.foo.bar')
        self.session.install_action(CommandLookupTests.ReturnAction('sesnum', 'SESSION'), '.session')

    def test_hierarchy_lookup(self):
        num_cmd = Command('num')
        num_cmd.target = NodePath('.')
        self.assertEqual(self.interpreter.execute(num_cmd), 'ROOT')

        num_cmd.target = NodePath('.foo')
        self.assertEqual(self.interpreter.execute(num_cmd), 'FOO')

        num_cmd.target = NodePath('.foo.bar')
        self.assertEqual(self.interpreter.execute(num_cmd), 'BAR')

        num_cmd.target = NodePath('.session')
        self.assertEqual(self.interpreter.execute(num_cmd), 'ROOT')

    def test_alternative_lookup(self):
        sesnum_cmd = Command('sesnum')
        sesnum_cmd.target = NodePath('.')
        self.assertEqual(self.interpreter.execute(sesnum_cmd), 'SESSION')

        sesnum_cmd.target = NodePath('.foo.bar')
        self.assertEqual(self.interpreter.execute(sesnum_cmd), 'SESSION')

        sesnum_cmd.target = NodePath('.session')
        self.assertEqual(self.interpreter.execute(sesnum_cmd), 'SESSION')


if __name__ == '__main__':
    unittest.main()

