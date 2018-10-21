import unittest


class TokenizerTests(unittest.TestCase):
    def tok_test(self, text: str, expected_tokens: list):
        from contextshell.command import tokenize
        self.assertListEqual(expected_tokens, tokenize(text))

    def test_empty(self):
        self.tok_test("",
                      [])

    def test_just_action(self):
        self.tok_test("action",
                      ['action'])

    def test_target_path(self):
        self.tok_test("target: action",
                      ['target', ':', 'action'])

    def test_action_arguments(self):
        self.tok_test("action arg1 arg2",
                      ['action', 'arg1', 'arg2'])

    def test_scopes(self):
        self.tok_test("{target}: {action} {foo: bar}",
                      ['{', 'target', '}', ':',
                       '{', 'action', '}',
                       '{', 'foo', ':', 'bar', '}'])

    def test_single_quotes(self):
        self.tok_test("'foo'",
                      ['foo'])

    def test_double_quotes(self):
        self.tok_test("\"foo\"",
                      ['foo'])

    def test_spaces_in_string(self):
        self.tok_test("\"  foo bar \"",
                      ['  foo bar '])

    def test_integer(self):
        self.tok_test("123",
                      [123])

    def test_float(self):
        self.tok_test("3.1415",
                      [3.1415])

    def test_path(self):
        # CHECK: Not sure if this works 'right'
        from contextshell.path import NodePath
        self.tok_test("foo.bar",
                      [NodePath("foo.bar")])


def create_parser():
    """Create CommandParser instance for tests"""
    from contextshell.command import CommandParser
    return CommandParser()


class StringRepresentationTests(unittest.TestCase):
    def test_string_representation_contains_action_name(self):
        parser = create_parser()
        action_name = 'action'
        cmd = parser.parse(action_name)

        have_action_string = action_name in str(cmd)

        self.assertTrue(have_action_string)

    def test_string_representation_contains_action_argument(self):
        parser = create_parser()
        action_argument = 'arg'
        cmd = parser.parse(f"action {action_argument}")

        have_argument_string = action_argument in str(cmd)

        self.assertTrue(have_argument_string)

    def test_string_representation_contains_target_path(self):
        parser = create_parser()
        target_path = 'foo.bar'
        cmd = parser.parse(f"{target_path}: action")

        have_target_path = target_path in str(cmd)

        self.assertTrue(have_target_path)


class ParsingTests(unittest.TestCase):
    def test_empty(self):
        parser = create_parser()

        cmd = parser.parse("")

        self.assertIsNone(cmd)

    def test_just_whitespaces(self):
        parser = create_parser()

        cmd = parser.parse("   ")

        self.assertIsNone(cmd)

    def test_line_starting_with_comment_is_ignored(self):
        parser = create_parser()

        cmd = parser.parse("# comment")

        self.assertIsNone(cmd)

    def test_line_starting_with_whitespace_and_comment_is_ignored(self):
        parser = create_parser()

        cmd = parser.parse("  # indented comment")

        self.assertIsNone(cmd)

    def test_action_name(self):
        parser = create_parser()

        cmd = parser.parse("action")

        self.assertEqual("action", cmd.name)

    def test_action_arguments(self):
        parser = create_parser()

        cmd = parser.parse("action arg1 arg2")

        self.assertListEqual(['arg1', 'arg2'], cmd.arguments)

    def test_target(self):
        parser = create_parser()

        cmd = parser.parse("target: action")

        self.assertEqual("target", cmd.target)

    def test_nested_action_name(self):
        parser = create_parser()

        cmd = parser.parse("{action}")

        self.assertEqual("action", cmd.name.name)

    def test_nested_arguments(self):
        parser = create_parser()

        cmd = parser.parse("action {nested_action}")

        self.assertEqual("nested_action", cmd.arguments[0].name)

    def test_nested_target(self):
        parser = create_parser()

        cmd = parser.parse("{target_action}: action")

        self.assertEqual("target_action", cmd.target.name)


class TypeConversionTests(unittest.TestCase):
    def test_parse_int(self):
        pass
