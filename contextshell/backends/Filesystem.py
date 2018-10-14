from pathlib import Path
from contextshell.NodePath import NodePath
from contextshell.backends.ActionExecutor import ActionExecutor, ActionArgsPack
from contextshell.backends.BuiltinExecutor import BuiltinExecutor
from contextshell.backends.Module import Module
from contextshell.CallableAction import CallableAction, action_from_function


class FilesystemRoot(BuiltinExecutor):
    def __init__(self, root_directory_path: str):
        super().__init__()
        self.root_directory_path = Path(root_directory_path)
        self.register_action(action_from_function(self.contains_action))

    def _node_path_to_path(self, path: NodePath) -> Path:
        return Path('').joinpath(*path)

    def contains_action(self, target: NodePath, path: str) -> bool:
        target_path = self._node_path_to_path(target)
        full_path = self.root_directory_path.joinpath(target_path, path)
        return full_path.exists()


class FilesystemModule(Module):
    pass
