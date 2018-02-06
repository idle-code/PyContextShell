from contextshell.CommandParser import CommandParser
from contextshell.NodePath import *


class Shell:
    """Makes interaction with user painless"""
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.parser = CommandParser()

    def execute(self, command_line: str):
        command = self.parser.parse(command_line)
        if command is None:
            return None
        # TODO: remove when RelativeLayer is fully operational
        if command.target is None:
            command.target = NodePath('.')
        return self.interpreter.execute(command)

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
