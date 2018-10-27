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

        node_value = self.execute(".node", "get")

        self.assertEqual(node_value, value)

    def test_str(self):
        value = 'DATA'
        self.create_node('node', value)

        node_value = self.execute(".node", "get")

        self.assertEqual(node_value, value)

    def test_int(self):
        value = 123
        self.create_node('node', value)

        node_value = self.execute(".node", "get")

        self.assertEqual(node_value, value)


class SetActionTests(NodeTreeActionsTestsBase):
    def test_str(self):
        self.create_node('node', 'INITIAL')

        self.execute(".node", "set", "CHANGED")

        new_value = self.get_node_value('node')
        self.assertEqual(new_value, 'CHANGED')

    def test_different_type(self):
        self.create_node('node', 'INITIAL')

        with self.assertRaises(TypeError):
            self.execute(".node", "set", 123)

    def test_no_initial_value(self):
        self.create_node('node')

        with self.assertRaises(TypeError):
            self.execute(".node", "set", 123)


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


class ListActionTests(NodeTreeActionsTestsBase):
    def test_empty(self):
        self.create_node('node')

        node_list = self.execute(".node", "list")

        self.assertListEqual(node_list, [])

    def test_normal(self):
        self.create_node('node.@attribute')
        self.create_node('node.normal')

        node_list = self.execute(".node", "list")

        self.assertListEqual(node_list, ['normal'])

    def test_attributes(self):
        self.create_node('node.@attribute')
        self.create_node('node.normal')

        attribute_list = self.execute(".node", "list.attributes")

        self.assertListEqual(attribute_list, ['@attribute'])

    def test_all(self):
        self.create_node('node.@attribute')
        self.create_node('node.normal')

        node_list = self.execute(".node", "list.all")

        self.assertListEqual(node_list, ['@attribute', 'normal'])


class ListActionsActionTests(NodeTreeActionsTestsBase):
    def test_builtin(self):
        action_list = self.execute(".", "list.actions")

        expected_actions = {
            'get',
            'set',
            'create',
            'contains',
            'list',
            'remove',
            'find'
        }
        self.assertSetEqual(expected_actions, set(action_list))


class RemoveActionsActionTests(NodeTreeActionsTestsBase):
    def test_root(self):
        with self.assertRaises(ValueError):
            self.execute(".", "remove")

    def test_target(self):
        self.create_node('node')

        self.execute(".node", "remove")

        self.assertFalse(self.node_exists('node'))

    def test_existing_argument(self):
        self.create_node('node')

        self.execute(".", "remove", "node")

        self.assertFalse(self.node_exists('node'))

    def test_nonexistent_argument(self):
        self.execute(".", "remove", "node")
