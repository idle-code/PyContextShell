from Command import Command
from NodePath import NodePath
from TreeView import TreeView


class CommandInterpreter:
    actions_branch_name = '@actions'

    def __init__(self, root: TreeView):
        self.root = root

    def execute(self, command: Command):
        target_path = NodePath.cast(self.evaluate(command.target))

        action_path = NodePath.cast(self.evaluate(command.name))
        #full_action_path = self.find_action(target_path, action_path)

        arguments = map(self.evaluate, command.arguments)

        return self.root.execute(target_path, action_path, *arguments)

    def evaluate(self, part):
        if isinstance(part, Command):
            return self.execute(part)
        return part

    # def find_action(self, target_path: NodePath, action_path: NodePath):
    #     action_path = NodePath.join(CommandInterpreter.actions_branch_name, action_path)
    #     while len(target_path) > 0:
    #         absolute_action_path = NodePath.join(target_path, action_path)
    #         if self.root.exists(absolute_action_path):
    #             return self.root.get(absolute_action_path)
    #         target_path = target_path.base_path
    #     return None
