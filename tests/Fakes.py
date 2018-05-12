from contextshell.NodePath import NodePath
from typing import Dict, Callable


class FakeTree:
    def __init__(self):
        self.node_map : Dict[NodePath, FakeTree] = dict()

    def get(self, path):
        return self.node_map[path]

    def exists(self, path):
        return path in self.node_map


class FakeAction:
    def __init__(self):
        self.called = False
        self.received_tree = None
        self.received_target = None
        self.received_action = None
        self.received_arguments = None
        self.return_value = None

    def __call__(self, tree, target, action, *arguments):
        self.called = True
        self.received_tree = tree
        self.received_target = target
        self.received_action = action
        self.received_arguments = arguments
        return self.return_value


class FakeActionFinder:
    def __init__(self, generate_missing=False):
        self.actions : Dict[str, Callable] = dict()
        self.generate_missing = generate_missing
        self.received_targets = []

    def make_action_path(self, target_path: NodePath, action_path: NodePath):
        raise NotImplementedError()

    def find_action(self, target_path: NodePath, action_path: NodePath):
        self.received_targets.append(target_path)
        action_name = str(action_path)
        if action_name not in self.actions and self.generate_missing:
            return FakeAction()
        return self.actions.get(action_name)
