from Command import *
from IntNode import *
from Node2 import *
from NodePath import NodePath
from ActionNode import ActionNode


def _to_path(value) -> NodePath:
    if isinstance(value, Node):
        value = value.value
    return NodePath.cast(value)


class TreeRoot(PyNode):
    def __init__(self):
        super().__init__()

    @action
    def create(self, target_node, name_node, value_node=None):
        name = name_node.value
        if not isinstance(name, str):
            raise ValueError("Name could only be str but is: {} ({})".format(type(name), name))

        value = None  # default empty node value
        if value_node is not None:
            value = value_node.value

        target_node.append(name, Node(value))

    @action(path='create.int')
    def create_int(self, target_node, name_node, value_node=None):
        # TODO: create type-registration system (so methods as this won't be needed)
        name = name_node.value
        if not isinstance(name, str):
            raise ValueError("Name could only be str but is: {} ({})".format(type(name), name))

        value = 0  # default int node value
        if value_node is not None:
            value = value_node.value

        target_node.append(name, IntNode(value))

    @action
    def get(self, target_node):
        return target_node.value

    @action
    def set(self, target_node, value_node):
        target_node.value = value_node.value

    @action(path='list.all')
    def list_all(self, target_node):
        return [node for node in target_node.subnodes]

    @action(path='list.names')
    def list_names(self, target_node):
        return [name for name in target_node.subnode_names]

    @action
    def list(self, target_node):
        return self.list_nodes(target_node)

    @action(path='list.nodes')
    def list_nodes(self, target_node):
        return [n for n in self.list_all(target_node) if not n['@name'].value.startswith('@')]

    @action(path='list.attributes')
    def list_attributes(self, target_node):
        return [n for n in self.list_all(target_node) if n['@name'].value.startswith('@')]

    @action(path='list.actions')
    def list_actions(self, target_node):
        if ActionNode.ActionsNodeName in target_node.subnode_names:
            return self.list(target_node[ActionNode.ActionsNodeName])
        return []

    @action(path='list.tree')
    def list_tree(self, target_node):
        paths = []
        for node in target_node.subnodes:
            if Node.is_virtual(node):  # So infinite nodes won't be generated
                continue
            paths.append(node.path)
            paths.extend(self.list_tree(node))
        return paths

    @action
    def delete(self, target_node, name_node):
        if not target_node.remove_node(name_node.value):
            raise NameError("Node {} does not exists".format(name_node.value))

    @action
    def contains(self, target_node, name_node):
        name = name_node.value
        return name in target_node.subnode_names

    @action
    def repr(self, target_node):
        return repr(target_node)

    def call(self, target_path, action_name, *action_parameters):
        # TODO: check if following type checks are necessary
        if not isinstance(target_path, str):
            raise TypeError("target_path should be string")
        if not isinstance(action_name, str):
            raise TypeError("action_name should be string")

        action_parameters = list(action_parameters)  # TODO: check if this conversion is needed
        cmd = Command(action_name)
        cmd.target = target_path
        cmd.arguments = action_parameters
        result = self.execute(cmd)
        if result is None:
            return None

        if isinstance(result, Node):
            result = result.value
        return result

    def execute(self, command: Command):
        if not isinstance(command, Command):
            raise TypeError("Tree can only execute Commands ({} given)".format(type(command)))

        # Resolve target node
        target_path = _to_path(self._evaluate(command.target))
        target_node = self[target_path]
        if target_node is None:
            raise NameError('Could not find target path: {}'.format(target_path))

        # Resolve command node
        action_name = _to_path(self._evaluate(command.name))
        action_node = self.find_action(target_path, action_name)
        if action_node is None:
            raise NameError('No action named: {}'.format(command.name))

        # Evaluate all arguments
        arguments = map(self._evaluate, command.arguments)

        return action_node(target_node, *arguments)

    def _evaluate(self, value) -> Node:
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

    def find_action(self, target_path: NodePath, action_path: NodePath):
        while True:
            candidate_path = NodePath.join(target_path, ActionNode.ActionsNodeName, action_path)
            candidate_node = NodePath.resolve(self, candidate_path)
            if candidate_node is not None:
                return candidate_node

            if len(target_path) == 0:
                break
            target_path.pop()
        # TODO: try other (system defined) search paths
        return None
