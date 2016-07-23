from Command import *
from Node import *
import Commands

class Tree(Node):
    def __init__(self):
        super(Tree, self).__init__()

        #TODO: add more generic way to populate @commands branch (in Node?)
        self.create('@commands', None)
        commands = self['@commands']
        commands.create('create', Commands.Create())
        commands.create('get', Commands.Get())
        commands.create('set', Commands.Set())
        commands.create('list', Commands.List())
        commands.create('repr', Commands.Repr())

    def execute(self, command : Command):
        # Resolve target node
        target_path = self._to_path(self._evaluate(command.target))
        target_node = self._resolve_path(target_path)
        if target_node == None:
            raise NameError('Could not evaluate target path: {}'.format(command.target))

        # Resolve command node
        command_name = self._to_path(self._evaluate(command.name))
        command_node = self.find_command(target_path, command_name)
        if command_node == None:
            raise NameError('No command named: {}'.format(command.name))

        # Evaluate all arguments
        arguments = map(self._evaluate, command.arguments)

        return command_node(target_node, *arguments)

    def _evaluate(self, value):
        #print('Evaluating:', value)
        if isinstance(value, Command):
            return self.execute(value)
        if isinstance(value, list): # for paths
            return value

        try:
            value = Node(eval(value))
        except NameError:
            value = Node(str(value))
        except TypeError:
            value = Node(str(value))

        return value

    def find_command(self, target_path : list, command_path : list):
        #print("Looking for '{}' from '{}'".format(command_path, target_path))
        while True:
            cp = target_path + ['@commands'] + command_path
            #print("  checking", cp)
            candidate_node = self._resolve_path(cp)
            if candidate_node != None:
                return candidate_node
            if len(target_path) == 0:
                break
            target_path.pop()
        return None

    def _resolve_path(self, path):
        if path == None:
            raise ValueError('Cannot resolve none path')

        current_node = self
        for name in path:
            #print("Resolving: " + name)
            current_node = current_node.get_subnode(name)
            if current_node == None:
                return None
        return current_node

    def _to_path(self, value):
        if isinstance(value, str):
            value = [value]
        elif isinstance(value, Node):
            value = value.get()

        if not isinstance(value, list):
            raise TypeError('Unsupported path type: ' + str(type(value)))
        return value

