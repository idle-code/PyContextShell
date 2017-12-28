from contextshell.NodePath import NodePath
from contextshell.session_stack.SessionLayer import SessionLayer


class CrudSessionLayer(SessionLayer):
    def execute(self, target: NodePath, action_name: NodePath, *args):
        method_name = str(action_name)
        if method_name not in ['execute']:
            method = getattr(self, method_name, None)
            if method is not None:
                return method(target, *args)

        return super().execute(target, action_name, *args)

    def get(self, target: NodePath, *args):
        return super().execute(target, 'get', *args)

    def set(self, target: NodePath, *args):
        return super().execute(target, 'set', *args)

    def list(self, target: NodePath, *args):
        return super().execute(target, 'list', *args)

    def exists(self, target: NodePath, *args):
        return super().execute(target, 'exists', *args)

    def create(self, target: NodePath, *args):
        return super().execute(target, 'create', *args)

    def remove(self, target: NodePath, *args):
        return super().execute(target, 'remove', *args)
