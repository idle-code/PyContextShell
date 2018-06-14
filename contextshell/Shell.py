from contextshell.CommandParser import CommandParser
from contextshell.NodePath import *
from contextshell.CommandInterpreter import CommandInterpreter


class Shell:
    """Makes interaction with user painless"""
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.parser = CommandParser()

    def execute(self, command_line: str) -> str:
        command = self.parser.parse(command_line)
        if command is None:
            return None
        # TODO: remove when RelativeLayer is fully operational
        # if command.target is None:
        #     command.target = NodePath('.')
        try:
            result = self.interpreter.execute(command)
            return self.format_result(result)
        except Exception as error:
            return self.format_error(error)

    def format_result(self, result) -> str:
        if result is None:
            return None
        if isinstance(result, list):
            if len(result) < 1:
                return None
            return "\n".join(map(str, result))
        return str(result)

    def format_error(self, error) -> str:
        return "{}: {}".format(type(error).__name__, error)
