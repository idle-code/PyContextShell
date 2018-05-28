import unittest


def create_executor(*args):
    from tests.functional.ScriptTestBase import TestExecutor
    return TestExecutor(*args)


class FakeShell:
    def __init__(self):
        self.executed_commands = []
        self.responses = dict()

    def execute(self, command_line: str):
        self.executed_commands.append(command_line)
        return self.responses.get(command_line)


class TestExecutorTests(unittest.TestCase):
    def test_with_output_and_no_command_throw(self):
        exec = create_executor(FakeShell())

        with self.assertRaises(ValueError):
            exec.test("output")

    def test_single_command_no_output(self):
        shell = FakeShell()
        exec = create_executor(shell)

        exec.test("> .: action")

        self.assertIn(".: action", shell.executed_commands)

    def test_multiple_commands_no_output(self):
        shell = FakeShell()
        shell.responses['foo'] = None
        shell.responses['bar'] = None
        exec = create_executor(shell)

        exec.test("""
                > foo
                > bar
                """)

        self.assertSequenceEqual([
            'foo',
            'bar',
        ], shell.executed_commands)

    def test_single_command_output_matches(self):
        shell = FakeShell()
        shell.responses['.: action'] = 'bar'
        exec = create_executor(shell)

        exec.test("""
        > .: action
        bar
        """)

    def test_single_command_multiline_output_matches(self):
        shell = FakeShell()
        shell.responses['.: action'] = 'bar\nspam'
        exec = create_executor(shell)

        exec.test("""
        > .: action
        bar
        spam
        """)

    def test_single_command_different_output(self):
        shell = FakeShell()
        shell.responses['.: action'] = 'bar'
        exec = create_executor(shell)

        with self.assertRaises(AssertionError):
            exec.test("""
            > .: action
            foo
            """)

    def test_single_command_multiline_output_differs(self):
        shell = FakeShell()
        shell.responses['.: action'] = 'bar\nspam'
        exec = create_executor(shell)

        with self.assertRaises(AssertionError):
            exec.test("""
            > .: action
            bar
            gruz
            """)

    def test_single_command_unexpected_output(self):
        shell = FakeShell()
        shell.responses['.: action'] = 'bar'
        exec = create_executor(shell)

        with self.assertRaises(AssertionError):
            exec.test("> .: action")
