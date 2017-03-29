from ActionNode import ActionNode
from Node2 import Node


def get(target: Node):
    return target.get()

def set(target: Node, new_value):
    target.set(new_value)

def list(target: Node):
    return target.list()

def create(target: Node, name: str, value=None):
    target.append(name, Node(value))

def remove(target: Node, name_to_remove: str):
    target.remove(name_to_remove)


class GetAction(ActionNode):
    def __init__(self):
        super().__init__(get)


class SetAction(ActionNode):
    def __init__(self):
        super().__init__(set)


class ListAction(ActionNode):
    def __init__(self):
        super().__init__(list)


class RemoveAction(ActionNode):
    def __init__(self):
        super().__init__(remove)

class CreateAction(ActionNode):
    def __init__(self):
        super().__init__(create)
