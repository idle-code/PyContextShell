from contextshell.NodePath import NodePath
from typing import Dict, Callable


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
    def __init__(self, generate_missing=False):
        self.actions : Dict[str, Callable] = dict()
        self.generate_missing = generate_missing

    def make_action_path(self, target_path: NodePath, action_path: NodePath):
        raise NotImplementedError()

    def find_action(self, target_path: NodePath, action_path: NodePath):
        action_name = str(action_path)
        if action_name not in self.actions and self.generate_missing:
            return lambda *args: None
        return self.actions.get(action_name)
