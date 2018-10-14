from typing import Callable
from contextshell.ActionExecutor import unpack_argument_tree, ActionArgsPack
from contextshell.Action import Action
from contextshell.NodePath import NodePath


class CallableAction(Action):
    def __init__(self, implementation: Callable, name: NodePath) -> None:
        super().__init__(name)
        self.implementation = implementation

    def invoke(self, target: NodePath, action: NodePath, arguments: ActionArgsPack):
        #print("Invoked with:", *args)
        args, kwargs = unpack_argument_tree(arguments)
        return self.implementation(target, *args, **kwargs)


def action_from_function(function_to_wrap: Callable) -> Action:
    action_name: str = function_to_wrap.__name__
    if action_name.endswith('_action'):
        action_name = action_name[:-len('_action')]
    action_path = NodePath.from_python_name(action_name)
    return CallableAction(function_to_wrap, action_path)
