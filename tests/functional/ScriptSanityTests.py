import unittest


def create_executor(*args):
    from tests.functional.TestExecutor import TestExecutor
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
        executor = create_executor(FakeShell())

        with self.assertRaises(ValueError):
            executor.test("output")

    def test_single_command_no_output(self):
        shell = FakeShell()
        executor = create_executor(shell)

        executor.test("$ .: action")

        self.assertIn(".: action", shell.executed_commands)

    def test_multiple_commands_no_output(self):
        shell = FakeShell()
        shell.responses['foo'] = None
        shell.responses['bar'] = None
        executor = create_executor(shell)

        executor.test("""
                $ foo
                $ bar
                """)

        self.assertSequenceEqual([
            'foo',
            'bar',
        ], shell.executed_commands)

    def test_single_command_output_matches(self):
        shell = FakeShell()
        shell.responses['.: action'] = 'bar'
        executor = create_executor(shell)

        executor.test("""
        $ .: action
        bar
        """)

    def test_single_command_multiline_output_matches(self):
        shell = FakeShell()
        shell.responses['.: action'] = 'bar\nspam'
        executor = create_executor(shell)

        executor.test("""
        $ .: action
        bar
        spam
        """)

    def test_single_command_different_output(self):
        shell = FakeShell()
        shell.responses['.: action'] = 'bar'
        executor = create_executor(shell)

        with self.assertRaises(AssertionError):
            executor.test("""
            $ .: action
            foo
            """)

    def test_single_command_multiline_output_differs(self):
        shell = FakeShell()
        shell.responses['.: action'] = 'bar\nspam'
        executor = create_executor(shell)

        with self.assertRaises(AssertionError):
            executor.test("""
            $ .: action
            bar
            gruz
            """)

    def test_single_command_unexpected_output(self):
        shell = FakeShell()
        shell.responses['.: action'] = 'bar'
        executor = create_executor(shell)

        with self.assertRaises(AssertionError):
            executor.test("$ .: action")
