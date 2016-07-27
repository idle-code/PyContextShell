from Node import *
from ActionNode import *

class Create(ActionNode):
    def __init__(self):
        super(Create, self).__init__()

    def __call__(self, target_node, name_node, value_node = None):
        name = name_node.value

        if value_node != None:
            value_node = value_node.value
        target_node.append_node(name, Node(value_node))

class Delete(ActionNode):
    def __init__(self):
        super(Delete, self).__init__()

    def __call__(self, target_node):
        target_node.parent.remove_node(target_node.name)

class Exists(ActionNode):
    def __call__(self, target_node, name_node):
        name = name_node.value
        return name in target_node

class Get(ActionNode):
    def __init__(self):
        super(Get, self).__init__()

    def __call__(self, target_node):
        return target_node.value

class Set(ActionNode):
    def __init__(self):
        super(Set, self).__init__()

    def __call__(self, target_node, value_node):
        value = value_node.value
        target_node.value = value

class List(ActionNode):
    def __init__(self):
        super(List, self).__init__()

    def __call__(self, target_node):
        return [node for node in target_node]

class Repr(ActionNode):
    def __init__(self):
        super(Repr, self).__init__()

    def __call__(self, target_node):
        return repr(target_node)

