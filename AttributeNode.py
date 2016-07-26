from Node import *
from PyNode import *

class AttributeNode(Node):
    def __init__(self, getter = None, setter = None):
        super().__init__()
        self.getter_function = getter
        self.setter_function = setter

    @property
    def value(self):
        return self.getter_function()

    @value.setter
    def value(self, new_value):
        self.setter_function(new_value)

def Attribute(get_function):
    def _decorator_name(function):
        """Helper method to generate attribute name for provided function (method)"""
        return '@' + function.__name__

    @CreatorFunction
    def get_creator(parent_node : Node):
        if _decorator_name(get_function) in parent_node:
            return
        attribute_node = AttributeNode(get_function.__get__(parent_node, type(parent_node)))
        parent_node.append_node('@' + get_function.__name__, attribute_node)

        #TODO: rewrite attribute to act like normal property
        #setattr(parent_node, get_function.__name__, property(get_function))

    def set_decorator(set_function):
        @CreatorFunction
        def set_creator(parent_node : Node):
            get_creator(parent_node) # Create Attribute node if setter is being decorated first
            parent_node[_decorator_name(get_function)].setter_function = set_function.__get__(parent_node, type(parent_node))
            #TODO: rewrite attribute to act like normal property
        return set_creator

    get_creator.setter = set_decorator
    return get_creator

