from Command import *
from Node import *
from NodePath import *

from itertools import takewhile, dropwhile


def _parse_arguments(iterator):
    args = ''.join(iterator)
    args = args.split(' ')
    args = [a for a in args if len(a) > 0]
    return args, iterator


def _parse_command_name(iterator):
    iterator = dropwhile(lambda c: c.isspace(), iterator)
    name = ''.join(takewhile(lambda c: not c.isspace(), iterator))
    return name, iterator


def _parse_target(iterator):
    path = ''.join(takewhile(lambda c: c != ':', iterator))
    path = NodePath(path)
    return path, iterator


class Shell:
    """Makes interaction with user painless"""
    def __init__(self, root: Node):
        from CommandParser import CommandParser
        self.parser = CommandParser()
        self._root = root
        self.current_path = NodePath()
        self.current_path.is_absolute = True

    def parse(self, command_line: str):
        return self.parser.parse(command_line)


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
