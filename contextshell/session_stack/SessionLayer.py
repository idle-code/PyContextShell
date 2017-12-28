from contextshell.NodePath import NodePath
from typing import List


class SessionLayer:
    def __init__(self):
        self.next_layer: 'SessionLayer' = None

    @property
    def session_actions(self):
        return []

    def execute(self, target: NodePath, action_name: NodePath, *args):
        return self.next_layer.execute(target, action_name, *args)

# TODO: find a better way to discover available actions (in individual session layers)
# TODO: reimplement session mechanism to allow implementation of network (remote tree) transport
# TODO: find a way to allow some commands low-level data-structure layout - 'is.link' is one example
# TODO: execute should take argument tree instead of list
