import unittest


class FakeInterpreter:
    execute_error = None
    execute_result = None
    command_to_execute = None

    def execute(self, command):
        self.command_to_execute = command
        if self.execute_error is not None:
            raise self.execute_error
        return self.execute_result


def create_shell(*args):
    from contextshell.shell import Shell
    return Shell(*args)


class ExecuteTests(unittest.TestCase):
    def test_empty_command_returns_none(self):
        shell = create_shell(FakeInterpreter())

        execute_result = shell.execute("")

        self.assertIsNone(execute_result)

    def test_comment_returns_none(self):
        shell = create_shell(FakeInterpreter())

        execute_result = shell.execute("#comment")

        self.assertIsNone(execute_result)

    def test_execute_result_is_string(self):
        interpreter = FakeInterpreter()
        interpreter.execute_result = 123
        shell = create_shell(interpreter)

        execute_result = shell.execute("action")

        self.assertEqual("123", execute_result)

    def test_error_is_string(self):
        interpreter = FakeInterpreter()
        interpreter.execute_error = NameError("Test")
        shell = create_shell(interpreter)

        execute_result = shell.execute("action")

        self.assertEqual("NameError: Test", execute_result)

    @unittest.skip("Not sure if this is right place for this functionality")
    def test_execute_when_command_have_no_target_appends_current_branch(self):
        interpreter = FakeInterpreter()
        # TODO: where to hold current working branch/path?
        shell = create_shell(interpreter)

        shell.execute("action")

        self.assertEqual(".target", interpreter.command_to_execute.target)


class FormatResultTests(unittest.TestCase):
    def test_format_none(self):
        interpreter = FakeInterpreter()
        shell = create_shell(interpreter)

        formatted_none = shell.format_result(None)

        self.assertIsNone(formatted_none)

    def test_format_empty_list(self):
        interpreter = FakeInterpreter()
        shell = create_shell(interpreter)

        formatted_none = shell.format_result([])

        self.assertIsNone(formatted_none)

    def test_format_boolean(self):
        interpreter = FakeInterpreter()
        shell = create_shell(interpreter)

        formatted_false = shell.format_result(False)

        self.assertEqual("False", formatted_false)

    def test_format_list(self):
        interpreter = FakeInterpreter()
        shell = create_shell(interpreter)

        formatted_list = shell.format_result(['foo', 'bar'])

        self.assertEqual("foo\nbar", formatted_list)


class FormatErrorTests(unittest.TestCase):
    def test_message_contains_exception_class(self):
        interpreter = FakeInterpreter()
        shell = create_shell(interpreter)
        error = NameError("Test")

        error_message = shell.format_error(error)

        self.assertIn("NameError", error_message)
