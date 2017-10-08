from contextshell.session_stack.CrudSessionLayer import CrudSessionLayer
from contextshell.NodePath import NodePath
from contextshell.session_stack.VirtualNodeLayer import VirtualNodeLayer
from contextshell.session_stack.SessionStorageLayer import SessionStorageLayer
from contextshell.ActionNode import ActionNode
from typing import List


class RelativeLayer(VirtualNodeLayer):
    """Layer responsible for providing relative navigation in tree"""
    session_current_path = NodePath.join(SessionStorageLayer.session_path, 'current_path')

    def __init__(self, start_path: NodePath):
        super().__init__(self.session_current_path)
        self.current_path: NodePath = NodePath.cast(start_path)

    @property
    def session_actions(self):
        return [PwdAction(), CdAction()]

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


class PwdAction(ActionNode):
    def __init__(self):
        super().__init__(NodePath('pwd'))

    def __call__(self, session: CrudSessionLayer, target: NodePath, *arguments):
        return session.get(RelativeLayer.session_current_path)


class CdAction(ActionNode):
    def __init__(self):
        super().__init__(NodePath('cd'))

    def __call__(self, session: CrudSessionLayer, target: NodePath, *arguments):
        path = target
        if len(arguments) == 1:
            path = NodePath.cast(arguments[0])
            print("Setting path to:", path)
            # TODO: check if there is more arguments?
        session.set(RelativeLayer.session_current_path, path)
