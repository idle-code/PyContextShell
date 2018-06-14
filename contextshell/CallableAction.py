from collections import OrderedDict
from typing import Callable, Dict, Union, Any, Tuple, List
from contextshell.TreeRoot import unpack_argument_tree, ActionArgsPack
from contextshell.Action import Action
from contextshell.NodePath import NodePath


class CallableAction(Action):
    def __init__(self, implementation: Callable, name: NodePath):
        super().__init__(name)
        self.implementation = implementation

    def invoke(self, target: NodePath, action: NodePath, arguments: ActionArgsPack):
        #print("Invoked with:", *args)
        args, kwargs = unpack_argument_tree(arguments)
        return self.implementation(target, *args, **kwargs)


def action_from_function(method_to_wrap: Callable) -> Action:
    action_name: str = method_to_wrap.__name__
    if action_name.endswith('_action'):
        action_name = action_name[:-len('_action')]
    action_name = action_name.replace('_', '.')
    return CallableAction(method_to_wrap, NodePath(action_name))
