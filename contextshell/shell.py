from typing import Optional

from contextshell.command import CommandParser


class Shell:
    """Makes interaction with user painless"""

    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.parser = CommandParser()

    def execute(self, command_line: str) -> Optional[str]:
        """Executes single command line and produces textual output"""
        command = self.parser.parse(command_line)
        if command is None:
            return None
        # TODO: remove when RelativeLayer is fully operational
        # if command.target is None:
        #     command.target = NodePath('.')
        try:
            result = self.interpreter.execute(command)
            return self.format_result(result)
        except Exception as error:  # pylint: disable=broad-except
            return self.format_error(error)

    # pylint: disable=no-self-use
    def format_result(self, result) -> Optional[str]:
        """Transform valid command execution result into text"""
        if result is None:
            return None
        if isinstance(result, list):
            if not result:
                return None
            return "\n".join(map(str, result))
        return str(result)

    # pylint: disable=no-self-use
    def format_error(self, error) -> str:
        """Transform command failure result into text"""
        return "{}: {}".format(type(error).__name__, error)
