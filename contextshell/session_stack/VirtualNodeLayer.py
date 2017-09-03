from contextshell.session_stack.SessionLayer import *
from typing import List


class VirtualNodeLayer(SessionLayer):
    """Layer allowing easy creation of virtual nodes"""

    def __init__(self, virtual_path: NodePath):
        super().__init__()
        self.virtual_path = virtual_path

    def on_get(self):
        raise NotImplementedError()

    def on_set(self, new_value):
        raise NotImplementedError()

    def get(self, path: NodePath):
        if path == self.virtual_path:
            return self.on_get()
        else:
            return self.next_layer.get(path)

    def set(self, path: NodePath, new_value):
        if path == self.virtual_path:
            self.on_set(new_value)
        else:
            self.next_layer.set(path, new_value)

    def list(self, path: NodePath) -> List[NodePath]:
        if path == self.virtual_path:
            return []
        path_list = self.next_layer.list(path)
        if path == self.virtual_path.base_path:
            path_list.append(self.virtual_path)
        return path_list

    def exists(self, path: NodePath) -> bool:
        if path == self.virtual_path:
            return True
        return self.next_layer.exists(path)

    def create(self, path: NodePath, value=None):
        if self.virtual_path.is_parent_of(path):
            raise RuntimeError("Cannot create in virtual nodes")
        return self.next_layer.create(path, value)

    def remove(self, path: NodePath):
        if path == self.virtual_path:
            raise RuntimeError("Cannot remove virtual nodes")
        return self.next_layer.remove(path)
