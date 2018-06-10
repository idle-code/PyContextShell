from collections import OrderedDict
from typing import Callable, Dict, Union, Any, Tuple, List

from contextshell.Action import Action
from contextshell.NodePath import NodePath


class CallableAction(Action):
    def __init__(self, implementation: Callable):
        self.implementation = implementation

    def __call__(self, target: NodePath, action: NodePath, arguments: Dict[Union[NodePath, int], Any]):
        args, kwargs = CallableAction.unpack_argument_tree(arguments)
        return self.implementation(target, action, *args, **kwargs)

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
