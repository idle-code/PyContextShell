from Node import *
from NodePath import *


class Shell:
    """Makes interaction with user painless"""
    def __init__(self, root: Node):
        from CommandParser import CommandParser
        from CommandInterpreter import CommandInterpreter
        self._root = root
        self.interpreter = CommandInterpreter(self._root)
        self.parser = CommandParser()

        self.current_path = NodePath()
        self.current_path.is_absolute = True

    def execute(self, command_line: str):
        command = self.parser.parse(command_line)
        if command is None:
            return None
        return self.interpreter.execute(command)

    @staticmethod
    def pretty_print(result):
        if isinstance(result, list):
            for r in result:
                if isinstance(r, Node):
                    print("[{}] {}\t = {}".format(r['@index'], r["@name"], r))
                else:
                    print("[{}] {}".format(r['@index'], r))
        else:
            print(result)
