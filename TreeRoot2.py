from NodePath import NodePath
from CommandInterpreter import CommandInterpreter
from BasicActions import *
from TreeView import TreeView


class TreeRoot(TreeView):
    def __init__(self):
        super().__init__()
        self.root = Node()
        self.root.append(CommandInterpreter.actions_branch_name, Node())
        actions_node = self.root[CommandInterpreter.actions_branch_name]
        actions_node.append('get', GetAction())
        actions_node.append('set', SetAction())
        actions_node.append('list', ListAction())
        actions_node.append('create', CreateAction())
        actions_node.append('remove', RemoveAction())

    def execute(self, target: NodePath, action, *arguments):
        pass

