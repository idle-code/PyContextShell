from pathlib import Path
from contextshell.NodePath import NodePath
from contextshell.backends.ActionExecutor import ActionExecutor, ActionArgsPack
from contextshell.backends.BuiltinExecutor import BuiltinExecutor
from contextshell.backends.Module import Module
from contextshell.CallableAction import CallableAction, action_from_function
from contextshell.exceptions import NotSupportedError


class FilesystemRoot(BuiltinExecutor):
    def __init__(self, root_directory_path: str):
        super().__init__()
        self.root_directory_path = Path(root_directory_path)
        self.register_action(action_from_function(self.contains_action))
        self.register_action(action_from_function(self.get_action))
        self.register_action(action_from_function(self.is_file_action))
        self.register_action(action_from_function(self.is_directory_action))
        self.register_action(action_from_function(self.list_action))

    def _to_os_path(self, *paths: NodePath) -> Path:
        node_paths = map(lambda p: NodePath(p), paths)
        os_paths = map(lambda p: Path('').joinpath(*p), node_paths)
        return self.root_directory_path.joinpath(*os_paths)

    def _to_node_path(self, os_path: Path) -> NodePath:
        raise NotImplementedError()

    def contains_action(self, target: NodePath, path: NodePath) -> bool:
        full_path = self._to_os_path(target, path)
        return full_path.exists()

    def get_action(self, target: NodePath):
        full_path = self._to_os_path(target)
        if full_path.is_dir():
            raise NotSupportedError("Operation not defined for directories")
        return full_path.read_text()

    def is_file_action(self, target: NodePath) -> bool:
        full_path = self._to_os_path(target)
        return full_path.is_file()

    def is_directory_action(self, target: NodePath) -> bool:
        full_path = self._to_os_path(target)
        return full_path.is_dir()

    def list_action(self, target: NodePath):
        dir_path = self._to_os_path(target)
        if not dir_path.is_dir():
            raise NotSupportedError("Operation not defined for files")
        return list(sorted([self._to_node_path(f) for f in dir_path.iterdir()]))


class FilesystemModule(Module):
    pass
