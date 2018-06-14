from collections import OrderedDict
from typing import Callable, Dict, Union, Any, Tuple, List

from contextshell.Action import Action
from contextshell.NodePath import NodePath


class CallableAction(Action):
    def __init__(self, implementation: Callable, name: NodePath):
        super().__init__(name)
        self.implementation = implementation

    def invoke(self, target: NodePath, action: NodePath, arguments: Dict[Union[NodePath, int], Any]):
        #print("Invoked with:", *args)
        args, kwargs = CallableAction.unpack_argument_tree(arguments)
        return self.implementation(target, *args, **kwargs)

    @staticmethod
    def unpack_argument_tree(arguments: Dict[Union[NodePath, int], Any]) -> Tuple[List[Any], Dict[NodePath, Any]]:
        args = list()
        kwargs = OrderedDict()
        for key, value in arguments.items():
            if isinstance(key, int):
                args.append(value)
            else:
                kwargs[key] = value
        return args, kwargs


def action_from_function(method_to_wrap: Callable) -> Action:
    action_name: str = method_to_wrap.__name__
    if action_name.endswith('_action'):
        action_name = action_name[:-len('_action')]
    action_name = action_name.replace('_', '.')
    return CallableAction(method_to_wrap, NodePath(action_name))
