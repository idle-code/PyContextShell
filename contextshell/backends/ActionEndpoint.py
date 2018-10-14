from abc import abstractmethod
from typing import Optional

from contextshell.backends.ActionExecutor import Action
from contextshell.backends.ActionExecutor import ActionExecutor, ActionArgsPack
from contextshell.NodePath import NodePath
from collections import OrderedDict


class ActionEndpoint(ActionExecutor):
    @abstractmethod
    def find_action(self, target: NodePath, action: NodePath) -> Optional[Action]:
        raise NotImplementedError()

    def execute(self, target: NodePath, action_name: NodePath, args: ActionArgsPack = None):
        if not args:
            args = OrderedDict()
        action_impl = self.find_action(target, action_name)
        if action_impl is None:
            raise NameError("Could not find action named '{}'".format(action_name))
        return action_impl.invoke(target, action_name, args)
