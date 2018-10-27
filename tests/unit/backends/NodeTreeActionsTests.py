from contextshell.path import NodePath

from .bases import ActionTestsBase


def create_node_tree(*args, **kwargs):
    from contextshell.backends.node import NodeTreeRoot
    return NodeTreeRoot()


class NodeTreeActionsTestsBase(ActionTestsBase):
    def create_node(self, name, value=None):
        node_path = NodePath(name, absolute=True)
        self.backend.create(node_path, value)

    def create_backend(self):
        return create_node_tree()


class ContainsActionTests(NodeTreeActionsTestsBase):
    def test_existing(self):
        self.create_node('node')

        exists = self.execute(".", "contains", 'node')

        self.assertTrue(exists)

    def test_existing_nested(self):
        self.create_node('parent.node')

        exists = self.execute(".", "contains", 'parent.node')

        self.assertTrue(exists)

    def test_nonexistent(self):
        exists = self.execute(".", "contains", 'nonexistent')

        self.assertFalse(exists)

    def test_nonexistent_nested(self):
        self.create_node('parent')

        exists = self.execute(".", "contains", 'parent.node')

        self.assertFalse(exists)
