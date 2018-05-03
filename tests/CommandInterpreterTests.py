import unittest
from Fakes import FakeAction, FakeActionFinder, FakeTree

from contextshell.CommandInterpreter import CommandInterpreter
from contextshell.NodePath import NodePath
from contextshell.Command import Command


class ExecuteTests(unittest.TestCase):
    def command(self, text: str) -> Command:
        from contextshell.CommandParser import CommandParser
        return CommandParser().parse(text)

    def test_execute_none_throws(self):
        interpreter = CommandInterpreter(action_finder=FakeActionFinder({}), tree=FakeTree())

        with self.assertRaises(ValueError):
            interpreter.execute(None)

    def test_execute_raises_when_action_could_not_be_found(self):
        action_finder = FakeActionFinder({})
        interpreter = CommandInterpreter(action_finder=action_finder, tree=FakeTree())
        unknown_cmd = self.command("unknown_action")

        with self.assertRaises(NameError):
            interpreter.execute(unknown_cmd)

    def test_execute_look_for_action(self):
        action_finder = FakeActionFinder({"action_name": lambda *a: None})
        interpreter = CommandInterpreter(action_finder=action_finder, tree=FakeTree())
        cmd = self.command("action_name")

        interpreter.execute(cmd)

        self.assertIn(NodePath('action_name'), action_finder.requested_action_paths)

    def test_execute_look_for_target_action(self):
        action_finder = FakeActionFinder({
            "target_action": lambda *a: None,
            "action_name": lambda *a: None
        })
        interpreter = CommandInterpreter(action_finder=action_finder, tree=FakeTree())
        cmd = self.command("{target_action}: action_name")

        interpreter.execute(cmd)

        self.assertIn(NodePath('target_action'), action_finder.requested_action_paths)

    def test_execute_look_for_arguments_action(self):
        action_finder = FakeActionFinder({
            "action_name": lambda *a: None,
            "argument_action1": lambda *a: None,
            "argument_action2": lambda *a: None,
        })
        interpreter = CommandInterpreter(action_finder=action_finder, tree=FakeTree())
        cmd = self.command("action_name {argument_action1} {argument_action2}")

        interpreter.execute(cmd)

        self.assertIn(NodePath('argument_action1'), action_finder.requested_action_paths)
        self.assertIn(NodePath('argument_action2'), action_finder.requested_action_paths)

    def test_execute_action(self):
        action = FakeAction()
        action_finder = FakeActionFinder({
            "action_name": action,
        })
        interpreter = CommandInterpreter(action_finder=action_finder, tree=FakeTree())
        cmd = self.command("action_name")

        interpreter.execute(cmd)

        self.assertIsNotNone(action.received_tree)
