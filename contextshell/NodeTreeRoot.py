from contextshell.Node import Node
from contextshell.NodePath import NodePath
from contextshell.TreeRoot import TreeRoot
from typing import Callable, List


# TODO: check how implement TemporaryTreeRoot (based on NodeTreeRoot)
class NodeTreeRoot(TreeRoot):
    """Frontend to the (passive) node-based data storage"""
    def __init__(self):
        self.root = self.create_node(None)
        from contextshell.ActionFinder import ActionFinder
        self.action_finder = ActionFinder(self)
        self.install_default_actions()

    def install_default_actions(self):
        def create(tree: NodeTreeRoot, target: NodePath, action: NodePath, name, value=None):
            tree.create(NodePath.join(target, name), value)

        self.action_finder.install_action(".", "create", create)

        def exists(tree: NodeTreeRoot, target: NodePath, action: NodePath, name):
            return tree.exists(NodePath.join(target, name))

        self.action_finder.install_action(".", "exists", exists)

        def get(tree: NodeTreeRoot, target: NodePath, action: NodePath):
            return tree.get(target)

        self.action_finder.install_action(".", "get", get)

        def set_action(tree: NodeTreeRoot, target: NodePath, action: NodePath, new_value):
            return tree.set(target, new_value)

        self.action_finder.install_action(".", "set", set_action)

        def list_action(tree: NodeTreeRoot, target: NodePath, action: NodePath):
            all_list = tree.list(target)
            return list(filter(lambda p: not self.is_attribute(p), all_list))

        self.action_finder.install_action(".", "list", list_action)

        def list_all(tree: NodeTreeRoot, target: NodePath, action: NodePath):
            return tree.list(target)

        self.action_finder.install_action(".", "list.all", list_all)

        def list_attributes(tree: NodeTreeRoot, target: NodePath, action: NodePath):
            all_list = tree.list(target)
            return list(filter(self.is_attribute, all_list))

        self.action_finder.install_action(".", "list.attributes", list_attributes)

        def list_actions(tree: NodeTreeRoot, target: NodePath, action: NodePath):
            # FIXME: use self.action_finder or other way of listing available actions
            from contextshell.ActionFinder import ActionFinder
            actions_branch = NodePath.join(target, ActionFinder.actions_branch_name)
            return tree.list(actions_branch)

        self.action_finder.install_action(".", "list.actions", list_actions)

        def remove(tree: NodeTreeRoot, target: NodePath, action: NodePath):
            return tree.remove(target)

        self.action_finder.install_action(".", "remove", remove)

    def is_attribute(self, path: NodePath):
        return path.startswith('@')

    def list_actions(self, path: NodePath) -> List[NodePath]:
        action_paths = self.list(NodePath.join(path, '@actions'))
        action_paths = sorted(action_paths)

        if len(path) == 0:  # Root
            return action_paths
        else:
            return action_paths + self.list_actions(path.base_path)

    def is_action(self, path: NodePath):
        node_value = self.get(path)
        return isinstance(node_value, Callable)

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
