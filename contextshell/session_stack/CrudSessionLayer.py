from contextshell.NodePath import NodePath
from typing import List


class SessionLayer:
    def __init__(self):
        self.next_layer: 'SessionLayer' = None

    @property
    def session_actions(self):
        return []

    def execute(self, target: NodePath, action_name: NodePath, *args):
        return self.next_layer.execute(target, action_name, *args)


class CrudSessionLayer(SessionLayer):
    def get(self, path: NodePath):
        return self.next_layer.get(path)

    def set(self, path: NodePath, new_value):
        return self.next_layer.set(path, new_value)

    def list(self, path: NodePath) -> List[NodePath]:
        return self.next_layer.list(path)

    def exists(self, path: NodePath) -> bool:
        return self.next_layer.exists(path)

    def create(self, path: NodePath, value=None):
        return self.next_layer.create(path, value)

    def remove(self, path: NodePath):
        return self.next_layer.remove(path)