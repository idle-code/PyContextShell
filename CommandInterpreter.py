from Command import Command
from Node import Node, NodePath
from ActionNode import ActionNode


class CommandInterpreter:
    def __init__(self, root: Node):
        self.root = root
        self.actions_branch_path = NodePath.cast('@actions')

    def execute(self, command: Command):
        target_path = NodePath.cast(self.evaluate(command.target))
        target_node = self.root[target_path]
        if target_node is None:
            raise NameError("Target path '{}' not found".format(target_path))

        action_path = NodePath.cast(self.evaluate(command.name))
        action_node = self.find_action(target_node, action_path)
        if action_node is None:
            raise NameError("Action named '{}' not found".format(action_path))

        arguments = map(self.evaluate, command.arguments)
        return action_node(target_node, *arguments)

    def evaluate(self, part):
        if isinstance(part, Command):
            return self.execute(part)
        return part

    def find_action(self, target: Node, path: NodePath) -> ActionNode:
        full_action_path = NodePath.join(self.actions_branch_path, path)
        while target is not None:
            if full_action_path in target:
                return target[full_action_path]
            if target.parent is None:
                break
            target = target.parent
        return None

