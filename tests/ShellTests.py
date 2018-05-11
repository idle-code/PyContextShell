import unittest


class FakeInterpreter:
    execute_result = None
    command_to_execute = None

    def execute(self, command):
        self.command_to_execute = command
        return self.execute_result


def create_shell(*args):
    from contextshell.Shell import Shell
    return Shell(*args)


class ShellTests(unittest.TestCase):
    def test_execute_with_empty_command_returns_none(self):
        shell = create_shell(FakeInterpreter())

        execute_result = shell.execute("")

        self.assertIsNone(execute_result)

    def test_execute_with_comment_returns_none(self):
        shell = create_shell(FakeInterpreter())

        execute_result = shell.execute("#comment")

        self.assertIsNone(execute_result)

    def test_execute_returns_execute_result(self):
        interpreter = FakeInterpreter()
        interpreter.execute_result = 123
        shell = create_shell(interpreter)

        execute_result = shell.execute("action")

        self.assertEqual(interpreter.execute_result, execute_result)

    @unittest.skip("Not sure if this is right place for this functionality")
    def test_execute_when_command_have_no_target_appends_current_branch(self):
        interpreter = FakeInterpreter()
        # TODO: where to hold current working branch/path?
        shell = create_shell(interpreter)

        shell.execute("action")

        self.assertEqual(".target", interpreter.command_to_execute.target)

