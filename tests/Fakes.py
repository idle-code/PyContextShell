from contextshell.NodePath import NodePath
from typing import Mapping, Callable


class FakeTree:
    pass


class FakeAction:
    def __init__(self):
        self.received_tree = None
        self.received_target_path = None
        self.received_arguments = None
        self.return_value = None

    def __call__(self, tree, target_path, *arguments):
        self.received_tree = tree
        self.received_target_path = target_path
        self.received_arguments = arguments
        return self.return_value


class FakeActionFinder:
    def __init__(self, actions : Mapping[str, Callable]):
        self.requested_action_paths = []
        self.actions = actions

    def make_action_path(self, target_path: NodePath, action_path: NodePath):
        raise NotImplementedError()

    def find_action(self, target_path: NodePath, action_path: NodePath):
        self.requested_action_paths.append(action_path)
        return self.actions.get(str(action_path))
