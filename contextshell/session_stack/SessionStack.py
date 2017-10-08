from contextshell.NodePath import NodePath
from contextshell.session_stack.CrudSessionLayer import CrudSessionLayer
from typing import List


class SessionStack(CrudSessionLayer):
    def __init__(self, storage_layer: CrudSessionLayer):
        super(SessionStack, self).__init__()
        if storage_layer is None:
            raise ValueError("Storage layer must be provided for session stack")
        self.layers = [storage_layer]

    def push(self, layer: CrudSessionLayer):
        if layer is None:
            raise ValueError("No layer to push provided")
        layer.next_layer = self.top
        self.layers.append(layer)

    def pop(self) -> CrudSessionLayer:
        if len(self.layers) == 1:
            raise RuntimeError("Storage layer cannot be removed from stack")
        removed_layer = self.layers.pop()
        removed_layer.next_layer = None
        return removed_layer

    @property
    def top(self) -> CrudSessionLayer:
        return self.layers[-1]

    def get(self, path: NodePath):
        return self.top.get(path)

    def set(self, path: NodePath, new_value):
        return self.top.set(path, new_value)

    def list(self, path: NodePath) -> List[NodePath]:
        return self.top.list(path)

    def exists(self, path: NodePath) -> bool:
        return self.top.exists(path)

    def create(self, path: NodePath, value=None):
        return self.top.create(path, value)

    def remove(self, path: NodePath):
        return self.top.remove(path)
