from Command import *
from Node import *
from NodePath import *

from itertools import takewhile, dropwhile

class Shell:
    def __init__(self, root : Node):
        self._root = root
        self.current_path = NodePath()
        self.current_path.isabsolute = True

    def parse(self, command_line):
        if command_line == None:
            return None

        command_line = command_line.strip()
        if len(command_line) == 0:
            return None # ignore empty lines

        if command_line.startswith('#'):
            return None # ignore comments

        i = iter(command_line)

        path = self.current_path
        if ':' in command_line:
            path, i = self._parse_target(i)

        command_name, i = self._parse_command_name(i)

        # Prepare command arguments:
        arguments, i = self._parse_arguments(i)

        #TODO: check if i is finished
        command = Command(path, command_name, arguments)
        #print(command)
        return command

    def _parse_target(self, iterator):
        path = ''.join(takewhile(lambda c: c != ':', iterator))
        path = NodePath(path)
        return path, iterator

    def _parse_command_name(self, iterator):
        spaces = ' \t\r\n'
        iterator = dropwhile(lambda c: c in spaces, iterator)
        name = ''.join(takewhile(lambda c: c not in spaces, iterator))
        return name, iterator

    def _parse_arguments(self, iterator):
        args = ''.join(iterator)
        args = args.split(' ')
        args = [a for a in args if len(a) > 0]
        return args, iterator

    @staticmethod
    def pretty_print(result):
        if isinstance(result, list):
            index = 0
            for r in result:
                print("[{}] {}\t = {}".format(index, r["@name"], r))
                index += 1
        else:
            print(result)


