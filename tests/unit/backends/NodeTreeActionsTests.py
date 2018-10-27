from contextshell.path import NodePath

from .bases import ActionTestsBase


def create_node_tree(*args, **kwargs):
    from contextshell.backends.node import NodeTreeRoot
    return NodeTreeRoot()


class NodeTreeActionsTestsBase(ActionTestsBase):
    def create_node(self, path, value=None):
        node_path = NodePath(path, absolute=True)
        self.backend.create(node_path, value)

    def get_node_value(self, path):
        node_path = NodePath(path, absolute=True)
        return self.backend.get(node_path)

    def node_exists(self, path) -> bool:
        node_path = NodePath(path, absolute=True)
        return self.backend.contains(node_path)

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


class GetActionTests(NodeTreeActionsTestsBase):
    def test_empty(self):
        value = None
        self.create_node('node', value)

        value = self.execute(".node", "get")

        self.assertEqual(value, value)

    def test_str(self):
        value = 'DATA'
        self.create_node('node', value)

        value = self.execute(".node", "get")

        self.assertEqual(value, value)

    def test_int(self):
        value = 123
        self.create_node('node', value)

        value = self.execute(".node", "get")

        self.assertEqual(value, value)


class CreateActionTests(NodeTreeActionsTestsBase):
    def test_empty(self):
        self.execute(".", "create", "node")

        self.assertTrue(self.node_exists('node'))
        node_value = self.get_node_value('node')
        self.assertEqual(node_value, None)

    def test_default_string_value(self):
        self.execute(".", "create", "node", "default value")

        self.assertTrue(self.node_exists('node'))
        node_value = self.get_node_value('node')
        self.assertEqual(node_value, "default value")

    def test_default_int_value(self):
        self.execute(".", "create", "node", 321)

        self.assertTrue(self.node_exists('node'))
        node_value = self.get_node_value('node')
        self.assertEqual(node_value, 321)
