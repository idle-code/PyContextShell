from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from .path import NodePath

ArgumentValue = Any  # pylint: disable=invalid-name
ActionArgsPack = Dict[Union[NodePath, int], ArgumentValue]
PositionalArguments = List[ArgumentValue]
KeywordArguments = Dict[str, ArgumentValue]


class Action(ABC):
    def __init__(self, name: NodePath) -> None:
        assert isinstance(name, NodePath)
        assert name.is_relative
        self.name: NodePath = name

    @abstractmethod
    def invoke(self, target: NodePath, action: NodePath, arguments: ActionArgsPack):
        raise NotImplementedError()


class CallableAction(Action):
    """Action with implementation based on python callables"""

    def __init__(self, implementation: Callable, name: NodePath) -> None:
        super().__init__(name)
        self.implementation = implementation

    def invoke(self, target: NodePath, action: NodePath, arguments: ActionArgsPack):
        # CHECK: why action name is not passed? Is it needed in the signature?
        args, kwargs = unpack_argument_tree(arguments)
        return self.implementation(target, *args, **kwargs)


def action_from_function(function_to_wrap: Callable) -> Action:
    action_name: str = function_to_wrap.__name__
    if action_name.endswith("_action"):
        action_name = action_name[: -len("_action")]
    action_path = NodePath.from_python_name(action_name)
    return CallableAction(function_to_wrap, action_path)


class Executor(ABC):
    @abstractmethod
    def execute(self, target: NodePath, action_name: NodePath, args: ActionArgsPack = None):
        raise NotImplementedError()


class ActionExecutor(Executor):
    """Interface for backends allowing execution of arbitrary actions"""

    def find_action(self, target: NodePath, action: NodePath) -> Optional[Action]:
        raise NotImplementedError()

    def execute(self, target: NodePath, action_name: NodePath, args: ActionArgsPack = None):
        if not args:
            args = OrderedDict()
        action_impl = self.find_action(target, action_name)
        if action_impl is None:
            raise NameError(f"Could not find action named '{action_name}'")
        return action_impl.invoke(target, action_name, args)


def unpack_argument_tree(
    action_args: ActionArgsPack
) -> Tuple[PositionalArguments, KeywordArguments]:
    args: Dict[int, ArgumentValue] = dict()
    kwargs: KeywordArguments = OrderedDict()
    for key, value in action_args.items():
        if isinstance(key, int):
            args[key] = value
        else:
            kwargs[key.to_python_name()] = value
    assert not args or max(args.keys()) < len(args) + len(kwargs)
    positional_args = [a[1] for a in sorted(args.items())]
    return positional_args, kwargs


def pack_argument_tree(*args: PositionalArguments, **kwargs: KeywordArguments) -> ActionArgsPack:
    pack_list: List[Tuple[Union[NodePath, int], ArgumentValue]] = []
    for i, arg in enumerate(args):
        pack_list.append((i, arg))
    for key, value in kwargs.items():
        pack_list.append((NodePath.from_python_name(key), value))
    return OrderedDict(pack_list)


class BuiltinExecutor(ActionExecutor):
    """Manages built-in, global action registry"""

    def __init__(self):
        super().__init__()
        self.builtin_actions: Dict[NodePath, Action] = {}

    def register_builtin_action(self, action: Action):
        if action is None:
            raise ValueError("No action to register provided")
        if action.name in self.builtin_actions:
            raise ValueError(f"Builtin action '{action.name}' already registered")
        self.builtin_actions[action.name] = action

    def list_builtin_actions(self) -> List[Action]:
        return list(self.builtin_actions.values())

    def find_action(self, target: NodePath, action: NodePath) -> Optional[Action]:
        return self.builtin_actions.get(action)
