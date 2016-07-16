from ContextNode import *
from CommandNode import *

class Create(CommandNode):
    def __init__(self):
        super(Create, self).__init__()

    def __call__(self, target, name, value = None):
        name = name.get()

        if value != None:
            value = value.get()
            #print("Setting {} value to {}".format(name, value))
        target.create(name, value)


class Get(CommandNode):
    def __init__(self):
        super(Get, self).__init__()

    def __call__(self, target):
        return target.get()

class Set(CommandNode):
    def __init__(self):
        super(Set, self).__init__()

    def __call__(self, target, value):
        value = value.get()
        target.set(value)

class List(CommandNode):
    def __init__(self):
        super(List, self).__init__()

    def __call__(self, target):
        return [node for node in target]

class Repr(CommandNode):
    def __init__(self):
        super(Repr, self).__init__()

    def __call__(self, target):
        return repr(target)

