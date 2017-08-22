from contextshell.session_stack.SessionLayer import SessionLayer
from contextshell.Node import Node
from contextshell.NodePath import NodePath
from typing import List

class StorageLayer(SessionLayer):
    def __init__(self, root: Node):
        self.root = root

    @staticmethod
    def _resolve(root: Node, path: NodePath) -> Node:
        path = NodePath.cast(path)
        if path.is_absolute:
            while root.parent is not None:
                root = root.parent
        if len(path) == 0:
            return root
        node = root.get_node(name=path[0])
        if node is None:
            return None
        return StorageLayer._resolve(node, NodePath.cast(path[1:]))

    def create(self, path: NodePath, value=None):
        path = NodePath.cast(path)
        parent_node = StorageLayer._resolve(self.root, path.base_path)
        if parent_node is None:
            raise NameError("Parent path doesn't exists: {}".format(path.base_path))
        parent_node.append(Node(value), path.base_name)

    def exists(self, path: NodePath) -> bool:
        node = StorageLayer._resolve(self.root, path)
        return node is not None

    def remove(self, path: NodePath):
        path = NodePath.cast(path)
        node = StorageLayer._resolve(self.root, path)
        if node is None:
            raise NameError("Node to remove doesn't exists: {}".format(path))
        parent_node = node.parent
        if parent_node is None:
            raise NameError("Cannot remove node without parent")
        parent_node.remove(path.base_name)

    def list(self, path: NodePath) -> List[str]:
        node = StorageLayer._resolve(self.root, path)
        if node is None:
            raise NameError("Node to list doesn't exists: {}".format(path))
        node_names = node.list()
        return list(map(lambda n: NodePath.join(path, n), node_names))

    def get(self, path: NodePath):
        node = StorageLayer._resolve(self.root, path)
        if node is None:
            raise NameError("Node doesn't exists: {}".format(path))
        return node.get()

    def set(self, path: NodePath, new_value):
        node = StorageLayer._resolve(self.root, path)
        if node is None:
            raise NameError("Node doesn't exists: {}".format(path))
        return node.set(new_value)
