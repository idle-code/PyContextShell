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
        return str(result)

    def format_error(self, error) -> str:
        return "{}: {}".format(type(error).__name__, error)

    @staticmethod
    def pretty_print(result):
        if isinstance(result, list):
            for elem in result:
                print(elem)
        else:
            print(result)
        # TODO: Rewrite to support new list format (and attributes)
        # if isinstance(result, list):
        #     for r in result:
        #         if isinstance(r, Node):
        #             print("[{}] {}\t = {}".format(r['@index'], r["@name"], r))
        #         else:
        #             print("[{}] {}".format(r['@index'], r))
        # else:
        #     print(result)
