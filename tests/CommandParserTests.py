import unittest
from CommandParser import CommandParser
from Command import Command


class CommandTokenizerTests(unittest.TestCase):
    def tok_test(self, text: str, expected_tokens: list):
        from CommandParser import tokenize
        self.assertListEqual(expected_tokens, tokenize(text))

    def test_empty(self):
        self.tok_test("",
                      [])

    def test_action(self):
        self.tok_test("action",
                      ['action'])

    def test_target(self):
        self.tok_test("target: action",
                      ['target', ':', 'action'])

    def test_args(self):
        self.tok_test("action arg1 arg2",
                      ['action', 'arg1', 'arg2'])

    def test_scopes(self):
        self.tok_test("{target}: {action} {foo: bar}",
                      ['{', 'target', '}', ':',
                       '{', 'action', '}',
                       '{', 'foo', ':', 'bar', '}'])


class CommandParserTests(unittest.TestCase):
    def setUp(self):
        self.parser = CommandParser()

    def parse(self, text) -> Command:
        cmd = self.parser.parse(text)
        if cmd is not None:
            # Check if parsed command can be rebuild:
            self.assertEqual(text, str(cmd))
        return cmd

    def test_empty(self):
        cmd = self.parse("")
        self.assertIsNone(cmd)

    def test_spaces(self):
        cmd = self.parse("   ")
        self.assertIsNone(cmd)

    def test_comments(self):
        cmd = self.parse("# rabarbar")
        self.assertIsNone(cmd)
        cmd = self.parse("  # indented")
        self.assertIsNone(cmd)

    def test_just_name(self):
        cmd = self.parse("action")
        self.assertEqual("action", cmd.name)

    def test_arguments(self):
        cmd = self.parse("action arg1 arg2")
        self.assertListEqual(['arg1', 'arg2'], cmd.arguments)

    def test_target(self):
        cmd = self.parse("target: action")
        self.assertEqual("target", cmd.target)
        self.assertEqual("action", cmd.name)

    def test_nested_target(self):
        cmd = self.parse("{target}: action")
        self.assertEqual("target", cmd.target.name)
        self.assertEqual("action", cmd.name)

    def test_nested_name(self):
        cmd = self.parse("{action}")
        self.assertIsInstance(cmd.name, Command)
        self.assertEqual("action", cmd.name.name)

    def test_nested_arguments(self):
        cmd = self.parse("action {foo} bar {spam: rabarbar}")
        self.assertEqual("action", cmd.name)
        self.assertIsInstance(cmd.arguments[0], Command)
        self.assertEqual("foo", cmd.arguments[0].name)
        self.assertEqual("bar", cmd.arguments[1])
        self.assertIsInstance(cmd.arguments[2], Command)
        self.assertEqual("spam", cmd.arguments[2].target)
        self.assertEqual("rabarbar", cmd.arguments[2].name)

if __name__ == '__main__':
    unittest.main()
