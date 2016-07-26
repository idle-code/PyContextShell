from Command import *
from Node import *
import Commands

class Tree(Node):
    def __init__(self):
        super(Tree, self).__init__()

        self.append_node('@commands', Node())
        commands = self['@commands']

        # Register standard commands:
        commands.append_node('create', Commands.Create())
        commands.append_node('get', Commands.Get())
        commands.append_node('set', Commands.Set())
        commands.append_node('list', Commands.List())
        commands.append_node('repr', Commands.Repr())
        #self.print()

    def create(self, path, value = None):
        node_path = NodePath(path, True)
        return self.call(node_path.branch_name, "create", node_path.base_name, value)

    def get(self, path):
        return self.call(path, "get")

    def set(self, path, value):
        return self.call(path, "set", value)

    def call(self, target_path, command_name, *command_parameters):
        command_parameters = list(command_parameters)
        result = self.execute(Command(target_path, command_name, command_parameters))
        if result == None:
            return None

        if isinstance(result, Node):
            result = result.value
        return result

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
        #print('Evaluating:', repr(value), type(value))
        if isinstance(value, Command):
            return self.execute(value)
        if isinstance(value, list): # for paths
            return value

        if value == None or isinstance(value, int) or isinstance(value, str):
            return Node(value)

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

