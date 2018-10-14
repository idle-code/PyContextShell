from abc import ABC, abstractmethod
from typing import Optional

from contextshell.Action import Action
from contextshell.ActionExecutor import ActionExecutor, ActionArgsPack
from contextshell.NodePath import NodePath
from collections import OrderedDict


class ActionEndpoint(ActionExecutor):
    @abstractmethod
    def find_action(self, target: NodePath, action: NodePath) -> Optional[Action]:
        raise NotImplementedError()

    def execute(self, target: NodePath, action_name: NodePath, args: ActionArgsPack = None):
        #print("Execute: {}: {} {}".format(target, action, args))
        if not args:
            args = OrderedDict()
        action_impl = self.find_action(target, action_name)
        if action_impl is None:
            raise NameError("Could not find action named '{}'".format(action_name))
        return action_impl.invoke(target, action_name, args)

