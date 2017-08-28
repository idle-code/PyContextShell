from contextshell.session_stack.SessionLayer import SessionLayer
from contextshell.Node import Node
from contextshell.NodePath import NodePath
from typing import List


class StorageLayer(SessionLayer):
    def __init__(self, root: Node):
        self.root = root

    @staticmethod
    def _relative_resolve(root: Node, path: NodePath) -> Node:
        if len(path) == 0:
            return root
        node = root.get_node(name=path[0])
        if node is None:
            return None
        return StorageLayer._relative_resolve(node, NodePath.cast(path[1:]))

    def resolve(self, path: NodePath) -> Node:
        path = NodePath.cast(path)
        if not path.is_absolute:
            raise NameError("Only absolute paths are expected by StorageLayer")
        return StorageLayer._relative_resolve(self.root, path)

    def create(self, path: NodePath, value=None):
        path = NodePath.cast(path)
        parent_node = self.resolve(path.base_path)
        if parent_node is None:
            raise NameError("Parent path doesn't exists: {}".format(path.base_path))
        parent_node.append(Node(value), path.base_name)

    def exists(self, path: NodePath) -> bool:
        node = self.resolve(path)
        return node is not None

    def remove(self, path: NodePath):
        path = NodePath.cast(path)
        node = self.resolve(path)
        if node is None:
            raise NameError("Node to remove doesn't exists: {}".format(path))
        parent_node = node.parent
        if parent_node is None:
            raise NameError("Cannot remove node without parent")
        parent_node.remove(path.base_name)

    def list(self, path: NodePath) -> List[str]:
        node = self.resolve(path)
        if node is None:
            raise NameError("Node to list doesn't exists: {}".format(path))
        node_names = node.list()
        return list(map(lambda n: NodePath.join(path, n), node_names))

    def get(self, path: NodePath):
        node = self.resolve(path)
        if node is None:
            raise NameError("Node doesn't exists: {}".format(path))
        return node.get()

    def set(self, path: NodePath, new_value):
        node = self.resolve(path)
        if node is None:
            raise NameError("Node doesn't exists: {}".format(path))
        return node.set(new_value)
