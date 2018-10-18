import unittest
from unittest.mock import Mock, ANY, call
from collections import OrderedDict
from contextshell.command import Command, CommandInterpreter


class FakeTreeRoot(Mock):
    def __init__(self):
        super().__init__()
        self.execute = Mock()
        self.execute.return_value = 'return_value'


class ExecuteTests(unittest.TestCase):
    def command(self, text: str) -> Command:
        from contextshell.command import CommandParser
        return CommandParser().parse(text)

    def test_execute_none_throws(self):
        interpreter = CommandInterpreter(tree=FakeTreeRoot())

        with self.assertRaises(ValueError):
            interpreter.execute(None)

    def test_executes_action(self):
        tree_root = FakeTreeRoot()
        interpreter = CommandInterpreter(tree=tree_root)
        cmd = self.command("target: action_name")

        interpreter.execute(cmd)

        tree_root.execute.assert_called_with("target", "action_name", OrderedDict())

    def test_executes_target_action(self):
        tree_root = FakeTreeRoot()
        interpreter = CommandInterpreter(tree=tree_root)
        tree_root.execute.return_value = "target.path"
        cmd = self.command("{target_target: target_action}: action")

        interpreter.execute(cmd)

        tree_root.execute.assert_any_call("target_target", "target_action", OrderedDict())

    def test_executes_argument_actions(self):
        tree_root = FakeTreeRoot()

        interpreter = CommandInterpreter(tree=tree_root)
        cmd = self.command("target: action {arg_target: argument_action1} {arg_target: argument_action2}")

        interpreter.execute(cmd)

        tree_root.execute.assert_has_calls([
            call("arg_target", "argument_action1", ANY),
            call("arg_target", "argument_action2", ANY)
        ])

    def test_execute_passes_target(self):
        tree_root = FakeTreeRoot()
        interpreter = CommandInterpreter(tree=tree_root)
        cmd = self.command("target.path: action")

        interpreter.execute(cmd)

        tree_root.execute.assert_called_with("target.path", ANY, ANY)

    def test_execute_no_target_throws(self):
        interpreter = CommandInterpreter(tree=FakeTreeRoot())
        cmd = self.command("action")

        with self.assertRaises(RuntimeError):
            interpreter.execute(cmd)

    def test_execute_passes_action_path(self):
        tree_root = FakeTreeRoot()
        interpreter = CommandInterpreter(tree=tree_root)
        cmd = self.command("target: action.path")

        interpreter.execute(cmd)

        tree_root.execute.assert_called_with(ANY, "action.path", ANY)

    def test_execute_passes_arguments(self):
        tree_root = FakeTreeRoot()
        interpreter = CommandInterpreter(tree=tree_root)
        cmd = self.command("target: action foo")

        interpreter.execute(cmd)

        tree_root.execute.assert_called_with(ANY, ANY, OrderedDict([(0, 'foo')]))

    def test_execute_passes_returned_value(self):
        tree_root = FakeTreeRoot()
        tree_root.execute.return_value = 3
        interpreter = CommandInterpreter(tree=tree_root)
        cmd = self.command("target: action")

        return_value = interpreter.execute(cmd)

        self.assertEqual(3, return_value)
