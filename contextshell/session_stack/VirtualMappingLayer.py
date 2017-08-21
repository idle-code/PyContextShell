from contextshell.session_stack.SessionLayer import *
from typing import List


class VirtualMappingLayer(SessionLayer):
    def __init__(self, virtual_path: NodePath, backing_path: NodePath):
        super().__init__()
        self.virtual_path = virtual_path
        self.backing_path = backing_path

    def start(self, underlying_layer: 'SessionLayer'):
        super().start(underlying_layer)

    def finish(self):
        pass  # self.remove(self.temp_path)

    def _rewrite_path(self, path: NodePath):
        path = NodePath.cast(path)
        if self.virtual_path.is_parent_of(path):
            return NodePath.join(self.backing_path, path.relative_to(self.virtual_path))
        else:
            return path

    # def get(self, path: NodePath):
    #     return self.next_layer.get(path)
    #
    # def set(self, path: NodePath, new_value):
    #     return self.next_layer.set(path, new_value)

    def list(self, path: NodePath) -> List[NodePath]:
        return self.next_layer.list(self._rewrite_path(path)) + [self.virtual_path]

    def exists(self, path: NodePath) -> bool:
        return super().exists(self._rewrite_path(path))

    def create(self, path: NodePath, value=None):
        return self.next_layer.create(self._rewrite_path(path), value)

    # def remove(self, path: NodePath):
    #     return self.next_layer.remove(path)
