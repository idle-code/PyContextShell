from contextshell.NodePath import NodePath
from contextshell.session_stack.SessionLayer import SessionLayer
from typing import List


class SessionStack(SessionLayer):
    def __init__(self, storage_layer: SessionLayer):
        super(SessionStack, self).__init__()
        if storage_layer is None:
            raise ValueError("Storage layer must be provided for session stack")
        self.layers = [storage_layer]

    def start(self, underlying_layer: SessionLayer):
        if underlying_layer is not None:
            raise ValueError("Session stack cannot be on top on another one")

        previous_layer = None
        for layer in self.layers:
            layer.start(previous_layer)
            previous_layer = layer

    def push(self, layer: SessionLayer):
        if layer is None:
            raise ValueError("No layer to push provided")
        self.layers.append(layer)

    def pop(self) -> SessionLayer:
        if len(self.layers) == 1:
            raise RuntimeError("Storage layer cannot be removed from stack")
        return self.layers.pop()

    def finish(self):
        for layer in reversed(self.layers):
            layer.finish()

    @property
    def top(self) -> SessionLayer:
        return self.layers[-1]

    def get(self, path: NodePath):
        return self.top.get(path)

    def set(self, path: NodePath, new_value):
        return self.top.set(path, new_value)

    def list(self, path: NodePath) -> List[str]:
        return self.top.list(path)

    def exists(self, path: NodePath) -> bool:
        return self.top.exists(path)

    def create(self, path: NodePath, value=None):
        return self.top.create(path, value)

    def remove(self, path: NodePath):
        return self.top.remove(path)
