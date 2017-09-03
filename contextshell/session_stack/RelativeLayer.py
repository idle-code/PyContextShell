from contextshell.session_stack.VirtualNodeLayer import VirtualNodeLayer
from contextshell.session_stack.SessionLayer import *
from typing import List


class RelativeLayer(VirtualNodeLayer):
    """Layer responsible for providing relative navigation in tree"""

    def __init__(self, backing_path: NodePath, start_path: NodePath):
        super().__init__(backing_path)
        self.current_path: NodePath = NodePath.cast(start_path)

    def on_get(self):
        return self.current_path

    def on_set(self, new_value: NodePath):
        new_current_path = NodePath.cast(new_value)
        if not self.exists(new_current_path):
            raise ValueError("New current path doesn't exists")

        if new_current_path.is_absolute:
            self.current_path = new_value
        else:
            self.current_path = NodePath.join(self.current_path, new_value)

    def _rewrite_path(self, path: NodePath):
        path = NodePath.cast(path)
        if path.is_absolute:
            return path
        else:
            return NodePath.join(self.current_path, path)

    def get(self, path: NodePath):
        return super().get(self._rewrite_path(path))

    def set(self, path: NodePath, new_value):
        return super().set(self._rewrite_path(path), new_value)

    def list(self, path: NodePath) -> List[NodePath]:
        return super().list(self._rewrite_path(path))

    def exists(self, path: NodePath) -> bool:
        return super().exists(self._rewrite_path(path))

    def create(self, path: NodePath, value=None):
        return super().create(self._rewrite_path(path), value)

    def remove(self, path: NodePath):
        return super().remove(self._rewrite_path(path))
