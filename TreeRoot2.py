from CommandInterpreter import CommandInterpreter
from BasicActions import *


class TreeRoot(Node):
    def __init__(self):
        super().__init__()
        self.append(CommandInterpreter.actions_branch_name, Node())
        actions_node = self[CommandInterpreter.actions_branch_name]
        actions_node.append('get', GetAction())
        actions_node.append('set', SetAction())
        actions_node.append('list', ListAction())
        actions_node.append('create', CreateAction())
        actions_node.append('remove', RemoveAction())
