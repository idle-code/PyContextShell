from contextshell.Command import Command
from contextshell.NodePath import NodePath
from contextshell.TreeRoot import TreeRoot, parse_argument_tree
from typing import Dict, Union, Any


class CommandInterpreter:
    def __init__(self, tree: TreeRoot):
        self.tree = tree

    def execute(self, command: Command):
        if command is None:
            raise ValueError("No command to execute provided")
        target_path = self._evaluate(command.target)
        if target_path is None:
            raise RuntimeError("No action target specified")
        target_path = NodePath.cast(target_path)
        action_path = NodePath.cast(self._evaluate(command.name))
        arguments = list(map(self._evaluate, command.arguments))
        arguments = parse_argument_tree(arguments)
        return self.tree.execute(target_path, action_path, arguments)

    def _evaluate(self, part):
        if isinstance(part, Command):
            return self.execute(part)
        return part
