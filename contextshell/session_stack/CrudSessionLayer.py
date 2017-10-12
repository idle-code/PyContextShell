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
        if action_name == NodePath('get'):
            return self.get(target)
        elif action_name == NodePath('set'):
            self.set(target, args[0])
        elif action_name == NodePath('list'):
            return self.list(target)
        elif action_name == NodePath('exists'):
            tested_path = NodePath.join(target, args[0])
            return self.exists(tested_path)
        elif action_name == NodePath('create'):
            if len(args) == 2:
                return self.create(NodePath.join(target, args[0]), args[1])
            elif len(args) == 1:
                return self.create(NodePath.join(target, args[0]))
            else:
                raise RuntimeError("Too few arguments provided")
        elif action_name == NodePath('remove'):
            path_to_remove = NodePath.join(target, args[0])
            return self.remove(path_to_remove)

    def get(self, path: NodePath):
        return self.next_layer.execute(path, 'get')

    def set(self, path: NodePath, new_value):
        return self.next_layer.execute(path, 'set', new_value)

    def list(self, path: NodePath) -> List[NodePath]:
        return self.next_layer.execute(path, 'list')

    def exists(self, path: NodePath) -> bool:
        # FIXME: this will throw when path.base_path doesn't exists
        return self.next_layer.execute(path.base_path, 'exists', path.base_name)

    def create(self, path: NodePath, value=None):
        return self.next_layer.execute(path.base_path, 'create', NodePath(path.base_name), value)

    def remove(self, path: NodePath):
        return self.next_layer.execute(path.base_path, 'remove', path.base_name)
