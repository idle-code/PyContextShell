from contextshell.Node import Node
from contextshell.NodePath import NodePath
from contextshell.TreeRoot import TreeRoot, ActionArgsPack
from contextshell.Action import Action
from contextshell.CallableAction import action_from_function
from typing import List, Optional


# CHECK: how to implement TemporaryTreeRoot (based on NodeTreeRoot)
class NodeTreeRoot(TreeRoot):
    """Frontend to the (passive) node-based data storage"""
    def __init__(self):
        self.root = self.create_node(None)
        self.install_default_actions()

    def create_action(self, target: NodePath, path: str, value=None):  # NOCOVER
        self.create(NodePath.join(target, path), value)

    def contains_action(self, target: NodePath, path: str) -> bool:  # NOCOVER
        return self.contains(NodePath.join(target, path))

    def get_action(self, target: NodePath):  # NOCOVER
        return self.get(target)

    def set_action(self, target: NodePath, new_value):  # NOCOVER
        return self.set(target, new_value)

    def list_action(self, target: NodePath):  # NOCOVER
        all_list = self.list(target)
        return list(filter(lambda p: not self.is_attribute(p), all_list))

    def list_all_action(self, target: NodePath):  # NOCOVER
        return self.list(target)

    def list_attributes_action(self, target: NodePath):  # NOCOVER
        all_list = self.list(target)
        return list(filter(self.is_attribute, all_list))

    def list_actions_action(self, target: NodePath):  # NOCOVER
        # FIXME: use the same mechanism as in self.find_action
        # CHECK: consider using find.all.actions action
        actions_branch = NodePath.join(target, '@actions')
        return self.list(actions_branch)

    def remove_action(self, target: NodePath):  # NOCOVER
        # CHECK: use 'path' argument?
        return self.remove(target)

    def find_type_action(self, target: NodePath, type_name: str):  # NOCOVER
        return self.find_type(target, NodePath(type_name))

    def install_default_actions(self):
        self.install_global_action(action_from_function(self.create_action))
        self.install_global_action(action_from_function(self.contains_action))
        self.install_global_action(action_from_function(self.get_action))
        self.install_global_action(action_from_function(self.set_action))
        self.install_global_action(action_from_function(self.list_action))
        self.install_global_action(action_from_function(self.list_all_action))
        self.install_global_action(action_from_function(self.list_attributes_action))
        self.install_global_action(action_from_function(self.list_actions_action))
        self.install_global_action(action_from_function(self.remove_action))

        self.install_global_action(action_from_function(self.find_type_action))

    def install_global_action(self, action: Action):
        self.install_action(NodePath('.'), action)

    def install_action(self, target: NodePath, action: Action):
        self.create(NodePath.join(target, '@actions', action.name), action)

    def find_first_in(self, candidate_paths: List[NodePath]) -> Optional[Node]:
        if candidate_paths is None or len(candidate_paths) == 0:
            raise ValueError("No candidate paths provided")
        for path in candidate_paths:
            node = self._resolve_optional_path(path)
            if node is not None:
                return node
        return None

    def find_action(self, target: NodePath, action: NodePath) -> Optional[Action]:
        possible_locations = [
            NodePath.join(target, '@actions', action),
            NodePath.join(target, '@type.@actions', action),
            NodePath.join('.@actions', action)
        ]
        action_node = self.find_first_in(possible_locations)
        if action_node is None:
            # TODO: as last resort, try invoking 'find.action <action.name>'
            return None
        return action_node.get()

    def list_actions(self, path: NodePath) -> List[NodePath]:
        action_paths = self.list(NodePath.join(path, '@actions'))
        action_paths = sorted(action_paths)

        if len(path) == 0:  # Root
            return action_paths
        else:
            return action_paths + self.list_actions(path.base_path)

    def is_attribute(self, path: str): # CHECK: is used?
        return path.startswith('@')

    def install_global_type(self, node_type):
        self.install_type(NodePath('.'), node_type)

    def install_type(self, target: NodePath, node_type):
        self.create(NodePath.join(target, '@types', node_type.name), node_type)

    def find_type(self, target: NodePath, type_name: NodePath):  # TODO: add type-hints
        possible_locations = [
            NodePath.join(target, '@types', type_name),
            NodePath.join('.@types', type_name)
        ]
        type_node = self.find_first_in(possible_locations)
        if type_node is None:
            # TODO: as last resort, try invoking 'find.type <type.name>'
            return None
        return type_node.get()

    def execute(self, target: NodePath, action_name: NodePath, args: ActionArgsPack):
        #print("Execute: {}: {} {}".format(target, action, args))
        action_impl = self.find_action(target, action_name)
        if action_impl is None:
            raise NameError("Could not find action named '{}'".format(action_name))
        return action_impl.invoke(target, action_name, args)

    def create_node(self, value):
        return Node(value)

    def create(self, path: NodePath, initial_value=None):
        parent = self._create_path(path.base_path)
        new_node = self.create_node(initial_value)
        parent.append(new_node, path.base_name)

    def contains(self, path: NodePath) -> bool:
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

    def _resolve_optional_path(self, path: NodePath, root: Node=None) -> Optional[Node]:
        if root is None:
            if path.is_relative:
                raise ValueError("Could not resolve relative paths")
            root = self.root
            assert root is not None
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
            assert root is not None
        if len(path) == 0:
            return root

        next_branch_name = path[0]
        if not root.contains(next_branch_name):
            new_node = self.create_node(None)
            root.append(new_node, next_branch_name)
        return self._create_path(NodePath.cast(path[1:]), root.get_node(next_branch_name))
