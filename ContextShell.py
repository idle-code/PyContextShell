from ContextCommand import *
from ContextNode import *
from NodePath import *
from CommandNode import *

from itertools import takewhile, dropwhile

class ContextShell:
    def __init__(self, root : ContextNode):
        self._root = root
        self.current_path = NodePath()
        self.current_path.isabsolute = True

    def parse(self, command_line):
        i = iter(command_line)

        path = self.current_path
        if ':' in command_line:
            path, i = self._parse_target(i)

        command_name, i = self._parse_command_name(i)

        # Prepare command arguments:
        arguments, i = self._parse_arguments(i)

        #TODO: check if i is finished
        command = ContextCommand(path, command_name, arguments)
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

