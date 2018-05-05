import unittest
from unittest.mock import Mock, ANY
from Fakes import FakeAction, FakeActionFinder, FakeTree

from contextshell.CommandInterpreter import CommandInterpreter
from contextshell.NodePath import NodePath
from contextshell.Command import Command


class ExecuteTests(unittest.TestCase):
    def command(self, text: str) -> Command:
        from contextshell.CommandParser import CommandParser
        return CommandParser().parse(text)

    def test_execute_none_throws(self):
        interpreter = CommandInterpreter(action_finder=FakeActionFinder(generate_missing=True), tree=FakeTree())

        with self.assertRaises(ValueError):
            interpreter.execute(None)

    def test_execute_raises_when_action_could_not_be_found(self):
        action_finder = FakeActionFinder()
        interpreter = CommandInterpreter(action_finder=action_finder, tree=FakeTree())
        unknown_cmd = self.command("unknown_action")

        with self.assertRaises(NameError):
            interpreter.execute(unknown_cmd)

    def test_executes_action(self):
        action_finder = FakeActionFinder()
        action_finder.actions['action_name'] = action = Mock()
        interpreter = CommandInterpreter(action_finder=action_finder, tree=FakeTree())
        cmd = self.command("action_name")

        interpreter.execute(cmd)

        self.assertTrue(action.called)

    def test_executes_target_action(self):
        action_finder = FakeActionFinder(generate_missing=True)
        action_finder.actions['target_action'] = target_action = Mock()
        target_action.return_value = 'target_path'
        interpreter = CommandInterpreter(action_finder=action_finder, tree=FakeTree())
        cmd = self.command("{target_action}: action_name")

        interpreter.execute(cmd)

        self.assertTrue(target_action.called)

    def test_executes_argument_actions(self):
        action_finder = FakeActionFinder(generate_missing=True)
        action_finder.actions['argument_action1'] = arg1_action = Mock()
        action_finder.actions['argument_action2'] = arg2_action = Mock()
        interpreter = CommandInterpreter(action_finder=action_finder, tree=FakeTree())
        cmd = self.command("action_name {argument_action1} {argument_action2}")

        interpreter.execute(cmd)

        self.assertTrue(arg1_action.called)
        self.assertTrue(arg2_action.called)

    def test_execute_passes_tree_to_action(self):
        action_finder = FakeActionFinder()
        action_finder.actions['action'] = action = Mock()
        tree = FakeTree()
        interpreter = CommandInterpreter(action_finder=action_finder, tree=tree)
        cmd = self.command("action")

        interpreter.execute(cmd)

        action.assert_called_once_with(tree, ANY)

    def test_execute_passes_target_to_action(self):
        action_finder = FakeActionFinder()
        action_finder.actions['action'] = action = Mock()
        interpreter = CommandInterpreter(action_finder=action_finder, tree=FakeTree())
        cmd = self.command("target_path: action")

        interpreter.execute(cmd)

        action.assert_called_once_with(ANY, 'target_path')

    # TODO: what is passed when no target is specified as target? None?

    def test_execute_passes_arguments_to_action(self):
        action_finder = FakeActionFinder()
        action_finder.actions['action'] = action = Mock()
        interpreter = CommandInterpreter(action_finder=action_finder, tree=FakeTree())
        cmd = self.command("action foo bar")

        interpreter.execute(cmd)

        action.assert_called_once_with(ANY, None, 'foo', 'bar')

    def test_execute_passes_returned_value(self):
        assert False