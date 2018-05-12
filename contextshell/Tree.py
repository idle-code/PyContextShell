from contextshell.Node import Node
from contextshell.NodePath import NodePath


class Tree:
    def __init__(self, root_node: Node):
        if root_node is None:
            raise ValueError("No root node provided")
        self.root = root_node

    def create(self, path: NodePath, initial_value=None):
        if path.is_relative:
            raise ValueError("Relative path passed to create")
        pass

    def exists(self, path: NodePath) -> bool:
        return True

    def get(self, path: NodePath):
        return 3

