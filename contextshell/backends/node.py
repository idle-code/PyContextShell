from typing import List, Optional

from ..action import Action, ActionExecutor, action_from_function
from ..path import NodePath


class Node:
    def __init__(self, value=None):
        self._value = value
        self._subnodes = []  # TODO: use OrderedDict?
        self.parent = None

    def get(self):
        """Get value stored in this node"""
        return self._value

    def set(self, new_value):
        """Store provided value in this node"""
        if not isinstance(new_value, type(self._value)):
            new_type = type(new_value).__name__
            current_type = type(self._value).__name__
            raise TypeError(f"Cannot assign value with type '{new_type}' to '{current_type}' node")
        self._value = new_value

    def list(self):
        """List names of the subnodes"""
        names = map(lambda p: p[0], self._subnodes)
        index = 0
        indexed_names = []
        for name in names:
            indexed_names.append(name if name is not None else index)
            index += 1
        return indexed_names

    def append(self, node: "Node", name: str = None):
        """Append provided node as a subnode"""
        if node is None:
            raise ValueError("Cannot append None as node")
        if name is not None:
            if not name:
                raise NameError("Invalid appended node name - empty")
            if self.get_node(name) is not None:
                raise NameError(f"Node '{name}' already exists")
        node.parent = self
        self._subnodes.append((name, node))

    def get_node(self, name: str = None, index: int = None) -> Optional["Node"]:
        """Return subnode with provided name or index"""
        if name is not None:
            for name_node_pair in self._subnodes:
                if name_node_pair[0] == name:
                    return name_node_pair[1]
        elif index is not None:
            if 0 <= index < len(self._subnodes):
                return self._subnodes[index][1]
        else:
            raise NameError("No name or index provided")
        return None

    def __getitem__(self, name_or_index) -> "Node":
        """Return subnode with provided name or index"""
        if isinstance(name_or_index, int):
            node = self.get_node(index=name_or_index)
        else:
            node = self.get_node(name=name_or_index)
        if node is None:
            raise KeyError(name_or_index)
        return node

    def remove(self, name: str = None, index: int = None) -> "Node":
        """Remove subnode with provided name"""
        node_to_remove = self.get_node(name=name, index=index)
        if node_to_remove is None:
            raise NameError(f"Node '{name}' doesn't exists")
        self._subnodes = [p for p in self._subnodes if p[1] is not node_to_remove]
        node_to_remove.parent = None
        return node_to_remove

    def contains(self, name: str = None, index: int = None) -> bool:
        """Checks if there is a subnode with provided name"""
        return self.get_node(name=name, index=index) is not None

    def __contains__(self, name: str):
        return self.contains(name=name)


# CHECK: how to implement TemporaryTreeRoot (based on NodeTreeRoot)
class NodeTreeRoot(ActionExecutor):
    """Frontend to the (passive) node-based data storage"""

    def __init__(self):
        self.root = Node(None)
        self.install_default_actions()

    def create_action(self, target: NodePath, path: str, value=None):
        self.create(NodePath.join(target, path), value)

    def contains_action(self, target: NodePath, path: str) -> bool:
        return self.contains(NodePath.join(target, path))

    def get_action(self, target: NodePath):
        return self.get(target)

    def set_action(self, target: NodePath, new_value):
        return self.set(target, new_value)

    def list_action(self, target: NodePath):
        all_list = self.list(target)
        return list(filter(lambda p: not NodePath(p).is_attribute, all_list))

    def list_all_action(self, target: NodePath):
        return self.list(target)

    def list_attributes_action(self, target: NodePath):
        all_list = self.list(target)
        return list(filter(lambda p: NodePath(p).is_attribute, all_list))

    def list_actions_action(self, target: NodePath):
        # FIXME: use the same mechanism as in self.find_action
        # CHECK: consider using find.all.actions action
        actions_branch = NodePath.join(target, "@actions")
        return self.list(actions_branch)

    def remove_action(self, target: NodePath):
        # CHECK: use 'path' argument?
        return self.remove(target)

    def find_type_action(self, target: NodePath, type_name: str):
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
        self.install_action(NodePath("."), action)

    def install_action(self, target: NodePath, action: Action):
        self.create(NodePath.join(target, "@actions", action.name), action)

    def find_first_in(self, candidate_paths: List[NodePath]) -> Optional[Node]:
        if candidate_paths is None or not candidate_paths:
            raise ValueError("No candidate paths provided")
        for path in candidate_paths:
            node = self._resolve_optional_path(path)
            if node is not None:
                return node
        return None

    def find_action(self, target: NodePath, action: NodePath) -> Optional[Action]:
        possible_locations = [
            NodePath.join(target, "@actions", action),
            NodePath.join(target, "@type.@actions", action),
            NodePath.join(".@actions", action),
        ]
        action_node = self.find_first_in(possible_locations)
        if action_node is None:
            # TODO: as last resort, try invoking 'find.action <action.name>'
            return None
        return action_node.get()

    def list_actions(self, path: NodePath) -> List[NodePath]:
        action_paths = self.list(NodePath.join(path, "@actions"))
        action_paths = sorted(action_paths)

        if not path:  # Root
            return action_paths
        return action_paths + self.list_actions(path.base_path)

    def install_global_type(self, node_type):
        self.install_type(NodePath("."), node_type)

    def install_type(self, target: NodePath, node_type):
        self.create(NodePath.join(target, "@types", node_type.name), node_type)

    def find_type(self, target: NodePath, type_name: NodePath):  # TODO: add type-hints
        possible_locations = [
            NodePath.join(target, "@types", type_name),
            NodePath.join(".@types", type_name),
        ]
        type_node = self.find_first_in(possible_locations)
        if type_node is None:
            # TODO: as last resort, try invoking 'find.type <type.name>'
            return None
        return type_node.get()

    def create(self, path: NodePath, initial_value=None):
        parent = self._create_path(path.base_path)
        new_node = Node(initial_value)
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
            raise NameError(f"'{path}' doesn't exists")
        return node

    def _resolve_optional_path(self, path: NodePath, root: Node = None) -> Optional[Node]:
        if root is None:
            if path.is_relative:
                raise ValueError("Could not resolve relative paths")
            root = self.root
            assert root is not None
        if not path:
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
        if not path:
            return root

        next_branch_name = path[0]
        if not root.contains(next_branch_name):
            new_node = Node(None)
            root.append(new_node, next_branch_name)
        return self._create_path(NodePath.cast(path[1:]), root.get_node(next_branch_name))
