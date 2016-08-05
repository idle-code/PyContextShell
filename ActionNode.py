from Node import *
from PyNode import *
import functools

class ActionNode(Node):
    ActionsNodeName = '@actions'
    def __init__(self, callback = None):
        #TODO: check if passed prototype have right signature
        if callback == None:
            callback = self.__call__
        else:
            self.__call__ = callback
        super().__init__(callback)
        #self.value = callback

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

def Action(method=None, path=None):
    if not path:
        path = method.__name__

    # Apply str -> NodePath conversion if needed
    path = NodePath.cast(path)

    def decorator(method):
        method = NodeArgumentWrapper(method)

        @CreatorFunction
        def action_creator(parent_node : Node):
            if ActionNode.ActionsNodeName not in parent_node:
                parent_node.append_node(ActionNode.ActionsNodeName, Node())

            # Create path to the node if needed
            current_node = parent_node.create_path(NodePath.join(ActionNode.ActionsNodeName, path.base_path))

            # Bind method to instance (so it will become independent callable):
            bound_method = types.MethodType(method, parent_node)

            if path.base_name in current_node:
                # If subaction created path to node beforehand - we need to replace it
                # WARNING: this may cause undefined results when creating two actions with the same paths
                current_node.replace_node(path.base_name, ActionNode(bound_method))
            else:
                current_node.append_node(path.base_name, ActionNode(bound_method))

            return method # to restore original
        return action_creator

    if method:
        return decorator(method)
    else:
        return decorator

