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
        unknown_cmd = self.command("target: unknown_action")

        with self.assertRaises(NameError):
            interpreter.execute(unknown_cmd)

    def test_executes_action(self):
        action_finder = FakeActionFinder()
        action_finder.actions['action_name'] = action = FakeAction()
        interpreter = CommandInterpreter(action_finder=action_finder, tree=FakeTree())
        cmd = self.command("target: action_name")

        interpreter.execute(cmd)

        self.assertTrue(action.called)

    def test_executes_target_action(self):
        action_finder = FakeActionFinder(generate_missing=True)
        action_finder.actions['target_action'] = target_action = FakeAction()
        target_action.return_value = "target.path"
        interpreter = CommandInterpreter(action_finder=action_finder, tree=FakeTree())
        cmd = self.command("{target_target: target_action}: action")

        interpreter.execute(cmd)

        self.assertTrue(target_action.called)

    def test_executes_argument_actions(self):
        action_finder = FakeActionFinder(generate_missing=True)
        action_finder.actions['argument_action1'] = arg1_action = FakeAction()
        action_finder.actions['argument_action2'] = arg2_action = FakeAction()
        interpreter = CommandInterpreter(action_finder=action_finder, tree=FakeTree())
        cmd = self.command("target: action {arg_target: argument_action1} {arg_target: argument_action2}")

        interpreter.execute(cmd)

        self.assertTrue(arg1_action.called)
        self.assertTrue(arg2_action.called)

    def test_execute_passes_tree_to_action(self):
        action_finder = FakeActionFinder()
        action_finder.actions['action'] = action = FakeAction()
        tree = FakeTree()
        interpreter = CommandInterpreter(action_finder=action_finder, tree=tree)
        cmd = self.command("target: action")

        interpreter.execute(cmd)

        self.assertIs(tree, action.received_tree)

    def test_execute_passes_target_to_action(self):
        action_finder = FakeActionFinder()
        action_finder.actions['action'] = action = FakeAction()
        interpreter = CommandInterpreter(action_finder=action_finder, tree=FakeTree())
        cmd = self.command("target: action")

        interpreter.execute(cmd)

        self.assertEqual("target", action.received_target)

    def test_execute_no_target_throws(self):
        action_finder = FakeActionFinder()
        action_finder.actions['action'] = FakeAction()
        interpreter = CommandInterpreter(action_finder=action_finder, tree=FakeTree())
        cmd = self.command("action")

        with self.assertRaises(RuntimeError):
            interpreter.execute(cmd)

    def test_execute_passes_action_path_to_action(self):
        action_finder = FakeActionFinder()
        action_finder.actions['action.path'] = action = FakeAction()
        interpreter = CommandInterpreter(action_finder=action_finder, tree=FakeTree())
        cmd = self.command("target: action.path")

        interpreter.execute(cmd)

        self.assertEqual("action.path", action.received_action)

    def test_execute_passes_arguments_to_action(self):
        action_finder = FakeActionFinder()
        action_finder.actions['action'] = action = FakeAction()
        interpreter = CommandInterpreter(action_finder=action_finder, tree=FakeTree())
        cmd = self.command("target: action foo bar")

        interpreter.execute(cmd)

        self.assertSequenceEqual(['foo', 'bar'], action.received_arguments)

    def test_execute_passes_returned_value(self):
        action_finder = FakeActionFinder()
        action_finder.actions['return3'] = return3 = FakeAction()
        return3.return_value = 3
        interpreter = CommandInterpreter(action_finder=action_finder, tree=FakeTree())
        cmd = self.command("target: return3")

        return_value = interpreter.execute(cmd)

        self.assertEqual(3, return_value)
