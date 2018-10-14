from contextshell.NodePath import NodePath
from contextshell.TreeRoot import TreeRoot, ActionArgsPack
from contextshell.backends.Module import Module


class FilesystemRoot(TreeRoot):
    def __init__(self, root_directory_path: str):
        self.root_directory_path = root_directory_path

    def execute(self, target: NodePath, action: NodePath, args: ActionArgsPack = None):
        pass


class FilesystemModule(Module):
    pass
