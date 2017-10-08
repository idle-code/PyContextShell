from contextshell.ActionNode import *
from contextshell.session_stack.CrudSessionLayer import CrudSessionLayer
from typing import List


class GetAction(ActionNode):
    def __init__(self):
        super().__init__(path='get')

    def __call__(self, session: CrudSessionLayer, target: NodePath):
        return session.get(target)


class SetAction(ActionNode):
    def __init__(self):
        super().__init__(path='set')

    def __call__(self, session: CrudSessionLayer, target: NodePath, new_value):
        target_type = type(session.get(target))
        value_type = type(new_value)
        if value_type is not target_type:
            raise TypeError("Trying to set node with type {} to {}".format(target_type, value_type))
        session.set(target, new_value)


class ExistsAction(ActionNode):
    def __init__(self):
        super().__init__(path='exists')

    def __call__(self, session: CrudSessionLayer, target: NodePath, node_name: str) -> bool:
        return session.exists(NodePath.join(target, node_name))


class CreateAction(ActionNode):
    def __init__(self):
        super().__init__(path='create')

    def __call__(self, session: CrudSessionLayer, target: NodePath, name: str, value=None):
        path_to_create = NodePath.join(target, name)
        if session.exists(path_to_create):
            raise NameError("Path '{}' already exists".format(path_to_create))
        session.create(path_to_create, value)


class RemoveAction(ActionNode):
    def __init__(self):
        super().__init__(path='remove')

    def __call__(self, session: CrudSessionLayer, target: NodePath, node_name: str):
        path_to_remove = NodePath.join(target, node_name)
        if not session.exists(path_to_remove):
            raise NameError("Path '{}' doesn't exists".format(path_to_remove))
        session.remove(path_to_remove)


class ListAction(ActionNode):
    def __init__(self):
        super().__init__(path='list')

    def __call__(self, session: CrudSessionLayer, target: NodePath):
        # TODO: use link to list.nodes
        return self.list_nodes(session, target)

    @action(path='all')
    def list_all(self, session: CrudSessionLayer, target: NodePath):
        target_nodes = session.list(target)
        return ListAction._make_output_relative_to(target_nodes, target)

    @action(path='nodes')
    def list_nodes(self, session: CrudSessionLayer, target: NodePath):
        target_nodes = session.list(target)
        target_nodes = filter(lambda path: not ListAction._is_attribute(path), target_nodes)
        return ListAction._make_output_relative_to(target_nodes, target)

    @action(path='attributes')
    def list_attributes(self, session: CrudSessionLayer, target: NodePath):
        target_nodes = session.list(target)
        target_nodes = filter(lambda path: ListAction._is_attribute(path), target_nodes)
        return ListAction._make_output_relative_to(target_nodes, target)

    @staticmethod
    def _make_output_relative_to(target_list: List[NodePath], target: NodePath):
        target_list = map(lambda path: NodePath.join(target, path), target_list)
        return list(target_list)

    @staticmethod
    def _is_attribute(name: NodePath):
        return name.base_name.startswith('@')
