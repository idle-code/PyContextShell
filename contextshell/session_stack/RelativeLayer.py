from contextshell.session_stack.SessionLayer import *
from typing import List


class RelativeLayer(SessionLayer):
    """Layer responsible for providing relative navigation in tree"""

    def __init__(self, backing_path: NodePath, start_path: NodePath):
        super().__init__()
        self.backing_path = NodePath.cast(backing_path)
        self.start_path = NodePath.cast(start_path)

    @property
    def current(self):
        return self.get(self.backing_path)

    def start(self, underlying_layer: 'SessionLayer'):
        super().start(underlying_layer)
        self.create(self.backing_path, self.start_path)

    def _rewrite_path(self, path: NodePath):
        path = NodePath.cast(path)
        if path.is_absolute:
            return path
        else:
            return NodePath.join(self.current, path)

    def get(self, path: NodePath):
        return self.next_layer.get(self._rewrite_path(path))

    def set(self, path: NodePath, new_value):
        return self.next_layer.set(self._rewrite_path(path), new_value)

    def list(self, path: NodePath) -> List[NodePath]:
        return self.next_layer.list(self._rewrite_path(path))

    def exists(self, path: NodePath) -> bool:
        return self.next_layer.exists(self._rewrite_path(path))

    def create(self, path: NodePath, value=None):
        return self.next_layer.create(self._rewrite_path(path), value)

    def remove(self, path: NodePath):
        return self.next_layer.remove(self._rewrite_path(path))
