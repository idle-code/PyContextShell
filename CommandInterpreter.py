from Command import Command
from Node2 import Node
from NodePath import NodePath
from ActionNode import ActionNode


class CommandInterpreter:
    def __init__(self, root: Node):
        self.root = root
        self.actions_branch_name = '@actions'

    def execute(self, command: Command):
        target_path = NodePath.cast(self.evaluate(command.target))
        target_node = NodePath.resolve(self.root, target_path)
        if target_node is None:
            raise NameError("Target path '{}' not found".format(target_path))

        action_path = NodePath.cast(self.evaluate(command.name))
        action_node = self.find_action(target_node, action_path)
        if action_node is None:
            raise NameError("Action '{}' not found for target path: {}".format(action_path, target_path))

        arguments = map(self.evaluate, command.arguments)
        return action_node(target_node, *arguments)

    def evaluate(self, part):
        if isinstance(part, Command):
            return self.execute(part)
        return part

    def find_action(self, target: Node, path: NodePath) -> ActionNode:
        full_action_path = NodePath.join(self.actions_branch_name, path)
        while target is not None:
            action_node = NodePath.resolve(target, full_action_path)
            if action_node is not None:
                return action_node
            target = target.parent
        return None
