import unittest

from contextshell.command import Command


class CommandTests(unittest.TestCase):
    def test_initial_command_has_no_target(self):
        cmd = Command("action")

        self.assertEqual(None, cmd.target)

    def test_initial_command_has_no_arguments(self):
        cmd = Command("action")

        self.assertListEqual([], cmd.arguments)

    def test_initial_command_name_from_constructor(self):
        cmd = Command("action")

        self.assertEqual("action", cmd.name)

    def test_string_representation_contains_action_name(self):
        cmd = Command("action")

        command_representation = str(cmd)

        self.assertIn("action", command_representation)

    def test_string_representation_contains_arguments(self):
        cmd = Command("action")
        cmd.arguments = ["argument"]

        command_representation = str(cmd)

        self.assertIn("argument", command_representation)

    def test_string_representation_contains_target(self):
        cmd = Command("action")
        cmd.target = "target"

        command_representation = str(cmd)

        self.assertIn("target", command_representation)

    def test_string_representation_nested_target(self):
        cmd = Command("action")
        cmd.target = Command("target_action")

        command_representation = str(cmd)

        self.assertIn("{target_action}", command_representation)

    def test_string_representation_nested_action_name(self):
        cmd = Command(Command("name_action"))

        command_representation = str(cmd)

        self.assertIn("{name_action}", command_representation)

    def test_string_representation_nested_argument(self):
        cmd = Command("action")
        cmd.arguments = [Command("argument_action")]

        command_representation = str(cmd)

        self.assertIn("{argument_action}", command_representation)
