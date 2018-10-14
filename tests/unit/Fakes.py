from contextshell.NodePath import NodePath
from contextshell.backends.ActionExecutor import Action, ActionArgsPack
from typing import Dict


class FakeTree:
    def __init__(self):
        self.node_map : Dict[NodePath, FakeTree] = dict()

    def get(self, path):
        return self.node_map[path]

    def contains(self, path):
        return path in self.node_map


class FakeAction(Action):
    def __init__(self, name='action'):
        super().__init__(NodePath(name))
        self.called = False
        self.received_tree = None
        self.received_target = None
        self.received_action = None
        self.received_arguments = None
        self.return_value = None

    def invoke(self, target: NodePath, action: NodePath, arguments: ActionArgsPack):
        self.called = True
        self.received_target = target
        self.received_action = action
        self.received_arguments = arguments
        return self.return_value
