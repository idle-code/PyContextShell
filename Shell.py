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
        self._root = root
        self.current_path = NodePath()
        self.current_path.is_absolute = True

    def parse(self, command_line):
        if command_line is None:
            return None

        command_line = command_line.strip()
        if len(command_line) == 0:
            return None  # ignore empty lines

        if command_line.startswith('#'):
            return None  # ignore comments

        i = iter(command_line)

        path = self.current_path
        if ':' in command_line:
            path, i = _parse_target(i)

        command_name, i = _parse_command_name(i)

        # Prepare command arguments:
        arguments, i = _parse_arguments(i)

        # TODO: check if i is finished
        command = Command(path, command_name, arguments)
        #print(command)
        return command

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
