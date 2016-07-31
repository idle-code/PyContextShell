from Command import *
from PyNode import *
from ActionNode import *

class Tree(PyNode):
    def __init__(self):
        super().__init__()

    @Action
    def create(self, target_node, name_node, value_node = None):
        #parent_path = NodePath(target.value, True)
        name = name_node.value
        if not isinstance(name, str):
            raise ValueError("Name could only be str but is: {} ({})".format(type(name), name))

        value = None # default value
        if value_node != None:
            value = value_node.value

        target_node.append_node(name, Node(value))

    @Action
    def get(self, target_node):
        return target_node.value

    @Action
    def set(self, target_node, value_node):
        target_node.value = value_node.value

    @Action
    def list(self, target_node):
        return [node for node in target_node]

    @Action
    def delete(self, target_node, name_node):
        if not target_node.remove_node(name_node.value):
            raise NameError("Node {} does not exists".format(name_node.value))

    @Action
    def exists(self, target_node, name_node):
        name = name_node.value
        return name in target_node

    @Action
    def repr(self, target_node):
        return repr(target_node)


    def call(self, target_path, action_name, *action_parameters):
        if not isinstance(target_path, str):
            raise TypeError("target_path should be string")
        if not isinstance(action_name, str):
            raise TypeError("action_name should be string")

        action_parameters = list(action_parameters) #TODO: check if this conversion is needed
        result = self.execute(Command(target_path, action_name, action_parameters))
        if result == None:
            return None

        if isinstance(result, Node):
            result = result.value
        return result

    def execute(self, command : Command):
        if not isinstance(command, Command):
            raise TypeError('Tree can only execute Commands')

        # Resolve target node
        target_path = self._to_path(self._evaluate(command.target))
        target_node = self.resolve_path(target_path)
        if target_node == None:
            raise NameError('Could not find target path: {}'.format(target_path))

        # Resolve command node
        action_name = self._to_path(self._evaluate(command.name))
        action_node = self.find_action(target_path, action_name)
        if action_node == None:
            raise NameError('No action named: {}'.format(command.name))

        # Evaluate all arguments
        arguments = map(self._evaluate, command.arguments)

        return action_node(target_node, *arguments)

    def _evaluate(self, value) -> Node:
        #print('Evaluating:', repr(value), type(value))
        if isinstance(value, Command):
            return self.execute(value)
        elif isinstance(value, Node):
            return value
        raise TypeError("Cannot evaluate '{}' value to node".format(value))

    @staticmethod
    def _evaluate_to_node(value) -> Node:
        if isinstance(value, Node):
            return value
        return Node(value)

    def find_action(self, target_path : NodePath, action_path : NodePath):
        #print("Looking for '{}' from '{}'".format(action_path, target_path))
        while True:
            candidate_path = target_path + ['@actions'] + action_path
            #print("  checking", cp)
            candidate_node = self.resolve_path(candidate_path)
            if candidate_node != None:
                return candidate_node
            if len(target_path) == 0:
                break
            target_path.pop()
        return None

    def resolve_path(self, path):
        if path == None:
            raise ValueError('Cannot resolve none path')

        #TODO: add support for relative paths
        #if not path.isabsolute:
        #    raise ValueError('No support for relative paths yet: ' + str(path))

        current_node = self
        for name in path:
            #print("Resolving: " + name)
            current_node = current_node[name]
            if current_node == None:
                return None
        return current_node

    def _to_path(self, value) -> NodePath:
        if isinstance(value, Node):
            value = value.value
        return NodePath.cast(value)

