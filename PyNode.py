from Node2 import *
import types


def CreatorFunction(creator_function):
    creator_function.is_creator = True
    return creator_function


def is_creator(function):
    return hasattr(function, 'is_creator')


class PyNode(Node):
    def __init__(self, value=None):
        super().__init__(value)
        self._populate_subnodes()

    def _populate_subnodes(self):
        for field_name, field in sorted(type(self).__dict__.items()):
            if is_creator(field):
                #print("Creating node for:", field_name)
                original_field = field(self)
                bound_method = types.MethodType(original_field, self)
                setattr(self, field_name, bound_method)

