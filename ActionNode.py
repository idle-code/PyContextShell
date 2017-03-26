from Node2 import Node
from PyNode import *
from NodePath import NodePath
import functools


class ActionNode(Node):
    ActionsNodeName = '@actions'

    def __init__(self, callback=None):
        # TODO: check if passed prototype have right signature
        if callback is None:
            callback = self.__call__
        else:
            self.__call__ = callback
        super().__init__(callback)
        # self.value = callback

    def __call__(self, target, *arguments):
        callback = self.get()
        if callback is None:
            raise NotImplemented('__call__ method not overridden or no callback provided')
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
        # CHECK: wrap keyword arguments?
        return function(*args, **kwargs)

    return wrap_arguments


def action(method=None, path=None):
    if not path:
        path = method.__name__
    path = NodePath.cast(path)

    def decorator(decorated_method):
        decorated_method = NodeArgumentWrapper(decorated_method)

        @CreatorFunction
        def action_creator(parent_node: Node):
            # Create path to the node if needed
            current_node = NodePath.create_path(parent_node, NodePath.join(ActionNode.ActionsNodeName, path.base_path))

            # Bind method to instance, so it will become independent callable:
            bound_method = types.MethodType(decorated_method, parent_node)

            if current_node.contains(path.base_name):
                # If sub-action created path to node beforehand - we need to replace it
                # WARNING: this may cause undefined results when creating two actions with the same paths
                current_node.replace_node(path.base_name, ActionNode(bound_method))
            else:
                current_node.append(path.base_name, ActionNode(bound_method))

            return decorated_method  # to restore original

        return action_creator

    if method:
        return decorator(method)
    else:
        return decorator
