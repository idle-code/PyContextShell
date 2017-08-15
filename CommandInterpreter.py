from Command import Command
from NodePath import NodePath
from Session import Session


class CommandInterpreter:
    def __init__(self, root: Session):
        self.root = root

    def execute(self, command: Command):
        target_path = NodePath.cast(self.evaluate(command.target))
        action_path = NodePath.cast(self.evaluate(command.name))
        arguments = map(self.evaluate, command.arguments)
        return self.root.execute(target_path, action_path, *arguments)

    def evaluate(self, part):
        if isinstance(part, Command):
            return self.execute(part)
        return part
