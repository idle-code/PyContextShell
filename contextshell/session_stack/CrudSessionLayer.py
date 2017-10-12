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
    def execute(self, target: NodePath, action_name: NodePath, *args):
        method_name = str(action_name)
        if method_name not in ['execute']:
            method = getattr(self, method_name, None)
            if method is not None:
                return method(target, *args)

        return self.next_layer.execute(target, action_name, *args)

    def get(self, target: NodePath, *args):
        return self.next_layer.execute(target, 'get', *args)

    def set(self, target: NodePath, *args):
        return self.next_layer.execute(target, 'set', *args)

    def list(self, target: NodePath, *args):
        return self.next_layer.execute(target, 'list', *args)

    def exists(self, target: NodePath, *args):
        return self.next_layer.execute(target, 'exists', *args)

    def create(self, target: NodePath, *args):
        return self.next_layer.execute(target, 'create', *args)

    def remove(self, target: NodePath, *args):
        return self.next_layer.execute(target, 'remove', *args)
