from ContextCommand import *
from ContextNode import *
from NodePath import *
from CommandNode import *

from itertools import takewhile, dropwhile

class ContextShell:
    def __init__(self, root : ContextNode):
        self._root = root
        self.current_path = NodePath('.')

    def parse(self, command_line):
        #return command
        i = iter(command_line)

        # Resolve target node:
        path = self.current_path 
        if ':' in command_line:
            path, i = self._parse_path(i)
        target_node = self._resolve_path(path)

        # Resolve command to invoke:
        command, i = self._parse_command_name(i)
        command_node = self._resolve_command(command)

        # Prepare command arguments:
        arguments, i = self._parse_arguments(i)

        #TODO: check if i is finished
        return ContextCommand(target_node, command_node, arguments)

    def _parse_path(self, iterator):
        path = ''.join(takewhile(lambda c: c != ':', iterator))
        path = NodePath(path)
        return path, iterator

    def _resolve_path(self, path):
        if not path.isabsolute:
            path = NodePath(self.current_path + path)
            path.isabsolute = True
        return root[path]

    def _parse_command_name(self, iterator):
        spaces = ' \t\r\n'
        iterator = dropwhile(lambda c: c in spaces, iterator)
        name = ''.join(takewhile(lambda c: c not in spaces, iterator))
        return name, iterator

    def _resolve_command(self, command_name):
        return self._root[command_name]

    def _parse_arguments(self, iterator):
        args = ''.join(iterator)
        args = args.split(' ')
        args = [a for a in args if len(a) > 0]
        return args, iterator

#TESTING AREA
root = ContextNode()
root.create('get', CommandNode(lambda t, args: print('HELLO GET', t.get())))
root.create('test', 'rabarbar')
root.create('foo', 123)
root.print()

shell = ContextShell(root)
cmd = shell.parse('test:   get ja 123 tteeest')
print(cmd)
print(cmd.invoke())

cmd = shell.parse('foo: get ')
print(cmd)
print(cmd.invoke())
check why None appears at the end

