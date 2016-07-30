from Node import *
from PyNode import *
import functools

class ActionNode(Node):
    ActionNodeName = '@actions'
    def __init__(self, callback = None):
        super().__init__()
        #TODO: check if passed prototype have right signature
        if callback == None:
            callback = self.__call__
        else:
            self.__call__ = callback
        self.value = callback

    def __call__(self, target, *arguments):
        callback = self.value
        if callback == None:
            raise NotImplemented('__call__ method not overriden or no callback provided')
        return callback(target, *arguments)

def NodeArgumentWrapper(function):
    def wrap_arg(arg):
        if isinstance(arg, Node):
            return arg
        return Node(arg)

    @functools.wraps(function)
    def wrap_arguments(self, target_node, *args, **kwargs):
        if not isinstance(target_node, Node):
            raise TypeError('target_node should have Node type but is ' + str(type(target_node)))
        args = [self, target_node] + list(map(wrap_arg, args))
        #CHECK: wrap keyword arguments?
        return function(*args, **kwargs)

    return wrap_arguments

def Action(method):
    method = NodeArgumentWrapper(method)

    @CreatorFunction
    def action_creator(parent_node : Node):
        if ActionNode.ActionNodeName not in parent_node:
            parent_node.append_node(ActionNode.ActionNodeName, Node())

        # Bind method to instance:
        bound_method = types.MethodType(method, parent_node)

        actions_node = parent_node[ActionNode.ActionNodeName]
        actions_node.append_node(method.__name__, ActionNode(bound_method))
        return method # to restore original
    return action_creator

