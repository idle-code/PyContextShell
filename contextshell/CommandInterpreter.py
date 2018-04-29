from contextshell.Command import Command
from contextshell.NodePath import NodePath
from contextshell.ActionFinder import ActionFinder


class CommandInterpreter:
    def __init__(self, action_finder: ActionFinder, tree):
        self.action_finder = action_finder
        self.tree = tree

    def execute(self, command: Command):
        target_path = NodePath.cast(self._evaluate(command.target))
        action_path = NodePath.cast(self._evaluate(command.name))
        arguments = map(self._evaluate, command.arguments)
        action = self.action_finder.find_action(target_path, action_path)
        if action is None:
            raise NameError("Could not find action named '{}'".format(action_path))
        return action(self.tree, target_path, *arguments)

    def _evaluate(self, part):
        if isinstance(part, Command):
            return self.execute(part)
        return part
