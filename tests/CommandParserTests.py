import unittest
from CommandParser import CommandParser


class CommandParserTests(unittest.TestCase):
    def setUp(self):
        self.parser = CommandParser()

    def test_empty(self):
        self.parser.parse("command")
        self.assertEqual("command", self.parser.root.name)

    # def test_just_command(self):
    #     cmd = Command.parse("command")
    #     self.assertEqual("command", cmd.name)
    #
    # def test_command_args(self):
    #     cmd = Command.parse("command arg1 arg2")
    #     self.assertListEqual(['arg1', 'arg2'], cmd.arguments)
    #
    # def test_target(self):
    #     cmd = Command.parse("target: command")
    #     self.assertEqual("target", cmd.target)

if __name__ == '__main__':
    unittest.main()
