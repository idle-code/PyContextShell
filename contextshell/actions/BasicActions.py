from contextshell.ActionNode import *
from contextshell.session_stack.SessionLayer import SessionLayer


class GetAction(ActionNode):
    def __init__(self):
        super().__init__(path='get')

    def __call__(self, session: SessionLayer, target: NodePath):
        return session.get(target)


class SetAction(ActionNode):
    def __init__(self):
        super().__init__(path='set')

    def __call__(self, session: SessionLayer, target: NodePath, new_value):
        target_type = type(session.get(target))
        value_type = type(new_value)
        if value_type is not target_type:
            raise TypeError("Trying to set node with type {} to {}".format(target_type, value_type))
        session.set(target, new_value)


class ExistsAction(ActionNode):
    def __init__(self):
        super().__init__(path='exists')

    def __call__(self, session: SessionLayer, target: NodePath, node_name: str) -> bool:
        return session.exists(NodePath.join(target, node_name))


class CreateAction(ActionNode):
    def __init__(self):
        super().__init__(path='create')

    def __call__(self, session: SessionLayer, target: NodePath, name: str, value=None):
        path_to_create = NodePath.join(target, name)
        if session.exists(path_to_create):
            raise NameError("Path '{}' already exists".format(path_to_create))
        session.create(path_to_create, value)


class RemoveAction(ActionNode):
    def __init__(self):
        super().__init__(path='remove')

    def __call__(self, session: SessionLayer, target: NodePath, node_name: str):
        path_to_remove = NodePath.join(target, node_name)
        if not session.exists(path_to_remove):
            raise NameError("Path '{}' doesn't exists".format(path_to_remove))
        session.remove(path_to_remove)


class ListAction(ActionNode):
    def __init__(self):
        super().__init__(path='list')

    def __call__(self, session: SessionLayer, target: NodePath):
        # TODO: use link to list.nodes
        return self.list_nodes(session, target)

    @action(path='all')
    def list_all(self, session: SessionLayer, target: NodePath):
        return session.list(target)

    @action(path='nodes')
    def list_nodes(self, session: SessionLayer, target: NodePath):
        target_nodes = session.list(target)
        return [n for n in target_nodes if not ListAction._is_attribute(n)]

    @action(path='attributes')
    def list_attributes(self, session: SessionLayer, target: NodePath):
        target_nodes = session.list(target)
        return [n for n in target_nodes if ListAction._is_attribute(n)]

    @staticmethod
    def _is_attribute(name: str):
        return name.startswith('@')
