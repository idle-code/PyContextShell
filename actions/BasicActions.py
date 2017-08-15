from ActionNode import *


class GetAction(ActionNode):
    def __init__(self):
        super().__init__(path='get')

    def __call__(self, target: NodePath):
        return target.get()


class SetAction(ActionNode):
    def __init__(self):
        super().__init__(path='set')

    def __call__(self, target: NodePath, new_value):
        target.set(new_value)


class ExistsAction(ActionNode):
    def __init__(self):
        super().__init__(path='exists')

    def __call__(self, target: NodePath, node_name: str) -> bool:
        return target.contains(node_name)


class CreateAction(ActionNode):
    def __init__(self):
        super().__init__(path='create')

    def __call__(self, target: NodePath, name: str, value=None):
        target.append(Node(value), name)


class RemoveAction(ActionNode):
    def __init__(self):
        super().__init__(path='remove')

    def __call__(self, target: NodePath, node_name: str):
        target.remove(node_name)


class ListAction(ActionNode):
    def __init__(self):
        super().__init__(path='list')

    def __call__(self, target: NodePath):
        # TODO: use link to list.nodes
        return self.list_nodes(target)

    @action(path='all')
    def list_all(self, target: NodePath):
        return target.list()

    @action(path='nodes')
    def list_nodes(self, target: NodePath):
        return [n for n in target.list() if not ListAction._is_attribute(n)]

    @action(path='attributes')
    def list_attributes(self, target: NodePath):
        return [n for n in target.list() if ListAction._is_attribute(n)]

    @staticmethod
    def _is_attribute(name: str):
        return name.startswith('@')
