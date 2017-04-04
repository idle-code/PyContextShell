from ActionNode import *

class BasicActions:
    @staticmethod
    def get(target: Node):
        return target.get()

    @staticmethod
    def set(target: Node, new_value):
        target.set(new_value)

    @staticmethod
    def exists(target: Node, name: str) -> bool:
        return target.contains(name)

    @staticmethod
    def list(target: Node):
        return target.list()

    @staticmethod
    def create(target: Node, name: str, value=None):
        target.append(Node(value), name)

    @staticmethod
    def remove(target: Node, name_to_remove: str):
        target.remove(name_to_remove)


class ListAction(ActionNode):
    def __init__(self=None):
        super().__init__(path='list')

    def __call__(self, target: Node):
        # TODO: use link to list.nodes
        return self.list_nodes(target)

    @action(path='all')
    def list_all(self, target: Node):
        return target.list()

    @action(path='nodes')
    def list_nodes(self, target: Node):
        return [n for n in target.list() if not ListAction._is_attribute(n)]

    @action(path='attributes')
    def list_attributes(self, target: Node):
        return [n for n in target.list() if ListAction._is_attribute(n)]

    @staticmethod
    def _is_attribute(name: str):
        return name.startswith('@')
