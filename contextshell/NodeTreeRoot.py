from contextshell.Node import Node
from contextshell.NodePath import NodePath
from contextshell.TreeRoot import TreeRoot
from typing import Callable, Iterable


class NodeTreeRoot(TreeRoot):
    """Frontend to the (passive) node-based data storage"""
    def __init__(self):
        self.root = self.create_node(None)
        from contextshell.ActionFinder import ActionFinder
        self.action_finder = ActionFinder(self)

    def execute(self, target: NodePath, action: NodePath, *args):
        action_impl = self.action_finder.find_action(target, action)
        if action_impl is None:
            raise NameError("Could not find action named '{}'".format(action))
        return action_impl(self, target, action, *args)

    def create_node(self, value):
        return Node(value)

    def create(self, path: NodePath, initial_value=None):
        parent = self._create_path(path.base_path)
        new_node = self.create_node(initial_value)
        parent.append(new_node, path.base_name)

    def exists(self, path: NodePath) -> bool:
        return self._resolve_optional_path(path) is not None

    def get(self, path: NodePath):
        node = self._resolve_path(path)
        return node.get()

    def set(self, path: NodePath, new_value):
        node = self._resolve_path(path)
        node.set(new_value)

    def list(self, path: NodePath):
        node = self._resolve_path(path)
        return node.list()

    def remove(self, path: NodePath):
        node = self._resolve_path(path)
        if node.parent is None:
            raise ValueError("Could not remove root node")
        node.parent.remove(path.base_name)

    def _resolve_path(self, path: NodePath, root: Node = None) -> Node:
        node = self._resolve_optional_path(path, root)
        if node is None:
            raise NameError("'{}' doesn't exists".format(path))
        return node

    def _resolve_optional_path(self, path: NodePath, root: Node=None) -> Node:
        if root is None:
            if path.is_relative:
                raise ValueError("Could not resolve relative paths")
            root = self.root
        if len(path) == 0:
            return root

        next_branch_name = path[0]
        if not root.contains(next_branch_name):
            return None
        return self._resolve_optional_path(NodePath.cast(path[1:]), root.get_node(next_branch_name))

    def _create_path(self, path: NodePath, root: Node = None) -> Node:
        if root is None:
            if path.is_relative:
                raise ValueError("Could not resolve relative paths")
            root = self.root
        if len(path) == 0:
            return root

        next_branch_name = path[0]
        if not root.contains(next_branch_name):
            new_node = self.create_node(None)
            root.append(new_node, next_branch_name)
        return self._create_path(NodePath.cast(path[1:]), root.get_node(next_branch_name))
