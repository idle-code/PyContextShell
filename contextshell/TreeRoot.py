from abc import ABC, abstractmethod
from contextshell.NodePath import NodePath
from typing import Dict, Union, Any, Tuple, List
from collections import OrderedDict

ArgumentValue = Any
ActionArgsPack = Dict[Union[NodePath, int], ArgumentValue]
PositionalArguments = List[ArgumentValue]
KeywordArguments = Dict[str, ArgumentValue]


# CHECK: Rename TreeRoot to ActionEndpoint or something more appropriate?
class TreeRoot(ABC):
    @abstractmethod
    def execute(self, target: NodePath, action: NodePath, args: ActionArgsPack = None):
        raise NotImplementedError()


def unpack_argument_tree(action_args: ActionArgsPack) -> Tuple[PositionalArguments, KeywordArguments]:
    args: Dict[int, ArgumentValue] = dict()
    kwargs: KeywordArguments = OrderedDict()
    for key, value in action_args.items():
        if isinstance(key, int):
            args[key] = value
        else:
            kwargs[key.to_python_name()] = value
    assert len(args) == 0 or max(args.keys()) < len(args)+len(kwargs)
    positional_args = [a[1] for a in sorted(args.items())]
    return positional_args, kwargs


def pack_argument_tree(*args: PositionalArguments, **kwargs: KeywordArguments) -> ActionArgsPack:
    pack_list: List[Tuple[Union[NodePath, int], ArgumentValue]] = []
    for i, arg in enumerate(args):
        pack_list.append((i, arg))
    for key, value in kwargs.items():
        pack_list.append((NodePath.from_python_name(key), value))
    return OrderedDict(pack_list)


def parse_argument_tree(raw_arguments: List[str]) -> ActionArgsPack:
    from contextshell.CommandParser import convert_token_type
    pack_list: List[Tuple[Union[NodePath, int], ArgumentValue]] = []
    for i, arg in enumerate(raw_arguments):
        if isinstance(arg, str) and '=' in arg:
            key, value = arg.split('=')
            key_path = NodePath.from_python_name(key)
            if key_path.is_absolute:
                raise ValueError("Named argument path must be relative - {}".format(key_path))
            typed_value = convert_token_type(value)
            pack_list.append((key_path, typed_value))
        else:
            pack_list.append((i, arg))
    return OrderedDict(pack_list)
