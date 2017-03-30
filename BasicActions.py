from ActionNode import ActionNode
from Node2 import Node


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
        target.append(name, Node(value))

    @staticmethod
    def remove(target: Node, name_to_remove: str):
        target.remove(name_to_remove)


class GetAction(ActionNode):
    def __init__(self):
        super().__init__(BasicActions.get)


class SetAction(ActionNode):
    def __init__(self):
        super().__init__(BasicActions.set)


class ListAction(ActionNode):
    def __init__(self):
        super().__init__(BasicActions.list)


class RemoveAction(ActionNode):
    def __init__(self):
        super().__init__(BasicActions.remove)


class CreateAction(ActionNode):
    def __init__(self):
        super().__init__(BasicActions.create)
