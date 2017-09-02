from contextshell.session_stack.SessionLayer import *
from typing import List


class VirtualNodeLayer(SessionLayer):
    """Layer responsible for creating hard aliases of nodes in tree"""

    def __init__(self, virtual_path: NodePath, backing_path: NodePath):
        super().__init__()
        self.virtual_path = virtual_path
        self.backing_path = backing_path
        # TODO: validate that both paths are absolute and backing path exists

    def _rewrite_path(self, path: NodePath) -> NodePath:
        path = NodePath.cast(path)
        if self.virtual_path.is_parent_of(path):
            return NodePath.join(self.backing_path, path.relative_to(self.virtual_path))
        else:
            return path

    def _rewrite_path_to_virtual(self, path: NodePath) -> NodePath:
        path = NodePath.cast(path)
        if self.backing_path.is_parent_of(path):
            return NodePath.join(self.virtual_path, path.relative_to(self.backing_path))
        else:
            return path

    def get(self, path: NodePath):
        return self.next_layer.get(self._rewrite_path(path))

    def set(self, path: NodePath, new_value):
        return self.next_layer.set(self._rewrite_path(path), new_value)

    def list(self, path: NodePath) -> List[NodePath]:
        l = self.next_layer.list(self._rewrite_path(path))
        if self.virtual_path.is_parent_of(path):
            l = list(map(lambda n: self._rewrite_path_to_virtual(n), l))
        if NodePath.cast(path) == self.virtual_path.base_path:
            l += [self.virtual_path]
        return l

    def exists(self, path: NodePath) -> bool:
        return self.next_layer.exists(self._rewrite_path(path))

    def create(self, path: NodePath, value=None):
        return self.next_layer.create(self._rewrite_path(path), value)

    def remove(self, path: NodePath):
        return self.next_layer.remove(self._rewrite_path(path))
