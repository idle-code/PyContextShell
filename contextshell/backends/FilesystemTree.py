from pathlib import Path
from typing import List

from ..path import NodePath
from ..action import action_from_function, BuiltinExecutor
from ..exceptions import NotSupportedError


class FilesystemRoot(BuiltinExecutor):
    def __init__(self, root_directory_path: str):
        super().__init__()
        self.root_directory_path = Path(root_directory_path)
        self.register_builtin_action(action_from_function(self.contains_action))
        self.register_builtin_action(action_from_function(self.get_action))
        self.register_builtin_action(action_from_function(self.is_file_action))
        self.register_builtin_action(action_from_function(self.is_directory_action))
        self.register_builtin_action(action_from_function(self.list_action))
        self.register_builtin_action(action_from_function(self.list_actions_action))

    def _to_os_path(self, *paths: NodePath) -> Path:
        node_paths = map(lambda p: NodePath(p), paths)
        os_paths = map(lambda p: Path('').joinpath(*p), node_paths)
        return self.root_directory_path.joinpath(*os_paths)

    def contains_action(self, target: NodePath, path: NodePath) -> bool:
        full_path = self._to_os_path(target, path)
        return full_path.exists()

    def get_action(self, target: NodePath):
        full_path = self._to_os_path(target)
        if full_path.is_dir():
            return None
        return full_path.read_text()

    def is_file_action(self, target: NodePath) -> bool:
        full_path = self._to_os_path(target)
        return full_path.is_file()

    def is_directory_action(self, target: NodePath) -> bool:
        full_path = self._to_os_path(target)
        return full_path.is_dir()

    def list_action(self, target: NodePath) -> List[NodePath]:
        dir_path = self._to_os_path(target)
        if not dir_path.is_dir():
            return []
        return list(sorted([NodePath(f.name) for f in dir_path.iterdir()]))

    def list_actions_action(self, target: NodePath) -> List[NodePath]:
        # TODO: list actions depending on target type (might require issue #14)
        return list(map(lambda a: a.name, self.list_builtin_actions()))
