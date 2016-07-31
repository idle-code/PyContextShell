from Node import *
import functools
from pprint import pprint
import types

def CreatorFunction(creator_function):
    creator_function.is_creator = True
    return creator_function

def is_creator(function):
    return hasattr(function, 'is_creator')

def VirtualNode(generator_function=None, name=None):
    if not name: # called with generator_function
        name = generator_function.__name__
    elif not generator_function: # called with name parameter
        def VirtualNodeDecorator(gen_function):
            return gen_function
        generator_function = VirtualNodeDecorator
    else:
        raise RuntimeError('Invalid use of VirtualNode decorator')

    generator_function.is_node_generator = True
    generator_function.node_name = name
    return generator_function

def is_node_generator(function):
    return hasattr(function, 'is_node_generator')

class PyNode(Node):
    def __init__(self, value = None):
        super().__init__(value)
        self._populate_subnodes()

    def _populate_subnodes(self):
        for field_name, field in type(self).__dict__.items():
            if is_creator(field):
                #print("Creating node for:", field_name)
                original_field = field(self)
                bound_method = types.MethodType(original_field, self)
                setattr(self, field_name, bound_method)
            elif is_node_generator(field):
                #print("Creating node generator:", field.node_name)
                self.append_node_generator(field.node_name, field)

