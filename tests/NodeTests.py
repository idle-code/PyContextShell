import unittest

from contextshell.Node import Node


class ValueTests(unittest.TestCase):
    def test_constructor_sets_default_value_to_none(self):
        empty_node = Node()

        self.assertEqual(None, empty_node.get())

    def test_constructor_sets_provided_value(self):
        int_node = Node(123)

        self.assertEqual(123, int_node.get())

    def test_set_changes_value(self):
        int_node = Node(123)

        int_node.set(321)

        self.assertEqual(321, int_node.get())

    def test_set_throws_with_value_of_different_type(self):
        int_node = Node(123)

        with self.assertRaises(TypeError):
            int_node.set("string value")


class InitTests(unittest.TestCase):
    def test_new_node_have_no_subnodes(self):
        empty_node = Node()

        self.assertEqual(0, len(empty_node.list()))


class ListTests(unittest.TestCase):
    def test_list_contains_name(self):
        root = Node()
        node_name = 'foo'
        root.append(Node(), name=node_name)

        subnode_list = root.list()

        self.assertListEqual([node_name], subnode_list)

    def test_list_contains_index(self):
        root = Node()
        root.append(Node())

        subnode_list = root.list()

        self.assertListEqual([0], subnode_list)


class AppendTests(unittest.TestCase):
    def test_append_adds_name(self):
        root = Node()

        root.append(Node(), name='foo')

        self.assertEqual(1, len(root.list()))

    def test_append_sets_parent(self):
        root = Node()
        foo = Node()

        root.append(foo, name='foo')

        self.assertIs(foo.parent, root)

    def test_append_empty_name(self):
        root = Node()

        with self.assertRaises(NameError):
            root.append(Node(), name='')

    def test_append_none(self):
        root = Node()

        with self.assertRaises(ValueError):
            root.append(None, name='foo')

    def test_append_existing_name(self):
        root = Node()
        root.append(Node(), name='foo')

        with self.assertRaises(NameError):
            root.append(Node(), 'foo')

    @unittest.skip("This functionality is not needed")
    def test_append_existing_instance(self):
        root = Node()
        foo = Node()
        root.append(foo, name='foo1')

        with self.assertRaises(ValueError):
            root.append(foo, name='foo2')

    def test_append_anonymous_none(self):
        root = Node()

        with self.assertRaises(ValueError):
            root.append(None)


class GetNodeTests(unittest.TestCase):
    def test_get_node_no_args(self):
        root = Node()

        with self.assertRaises(NameError):
            root.get_node()

    def test_get_node_existing_by_name(self):
        root = Node()
        foo = Node()
        root.append(foo, name='foo')

        retrieved_foo_node = root.get_node(name='foo')

        self.assertIs(foo, retrieved_foo_node)

    def test_get_node_nonexistent_by_name(self):
        root = Node()

        retrieved_foo_node = root.get_node(name='nonexistent')

        self.assertIsNone(retrieved_foo_node)

    def test_get_node_existing_by_index(self):
        root = Node()
        child_node = Node()
        root.append(child_node)

        retrieved_node = root.get_node(index=0)

        self.assertIs(retrieved_node, child_node)

    def test_get_node_nonexistent_by_index(self):
        root = Node()

        retrieved_node = root.get_node(index=0)

        self.assertIsNone(retrieved_node)

    def test_get_node_negative_index(self):
        root = Node()

        retrieved_node = root.get_node(index=-3)

        self.assertIsNone(retrieved_node)


class GetItemTests(unittest.TestCase):
    def test_getitem_nonexistent_by_name(self):
        root = Node()

        with self.assertRaises(KeyError):
            root['nonexistent']

    def test_getitem_existing_by_name(self):
        root = Node()
        foo = Node()
        root.append(foo, name='foo')

        retrieved_foo_node = root['foo']

        self.assertIs(foo, retrieved_foo_node)

    def test_getitem_existing_by_index(self):
        root = Node()
        child_node = Node()
        root.append(child_node)

        retrieved_node = root[0]

        self.assertIs(retrieved_node, child_node)

    def test_getitem_nonexistent_by_index(self):
        root = Node()

        with self.assertRaises(KeyError):
            root[0]


class RemoveTests(unittest.TestCase):
    def test_remove_no_args(self):
        root = Node()

        with self.assertRaises(NameError):
            root.remove()

    def test_remove_returns_node(self):
        root = Node()
        foo = Node()
        root.append(foo, name='foo')

        removed_node = root.remove(name='foo')

        self.assertIs(foo, removed_node)

    def test_remove_clears_parent(self):
        root = Node()
        child_node = Node()
        root.append(child_node, name='child')

        removed_node = root.remove(name='child')

        self.assertIsNone(removed_node.parent)

    def test_remove_existing_name(self):
        root = Node()
        root.append(Node(), name='foo')

        root.remove(name='foo')

        self.assertEqual(0, len(root.list()))

    def test_remove_nonexistent_name(self):
        root = Node()

        with self.assertRaises(NameError):
            root.remove(name='nonexistent')

    def test_remove_existing_index(self):
        root = Node()
        child_node = Node()
        root.append(child_node)

        removed_node = root.remove(index=0)

        self.assertIs(removed_node, child_node)

    def test_remove_nonexistent_index(self):
        root = Node()

        with self.assertRaises(NameError):
            root.remove(index=0)


class ContainsTests(unittest.TestCase):
    def test_contains_existing(self):
        root = Node()
        root.append(Node(), name='foo')

        foo_exists = root.contains(name='foo')

        self.assertTrue(foo_exists)

    def test_contains_nonexistent(self):
        root = Node()

        nonexistent_exists = root.contains(name='nonexistent')

        self.assertFalse(nonexistent_exists)

    def test_contains_no_args(self):
        root = Node()

        with self.assertRaises(NameError):
            root.contains()

    def test_contains_existing_index(self):
        root = Node()
        root.append(Node())

        index_exists = root.contains(index=0)

        self.assertTrue(index_exists)

    def test_contains_nonexisting_index(self):
        root = Node()

        index_exists = root.contains(index=0)

        self.assertFalse(index_exists)


class ContainsOperatorTests(unittest.TestCase):
    def test_in_operator_existing(self):
        root = Node()
        root.append(Node(), name='foo')

        foo_exists = 'foo' in root

        self.assertTrue(foo_exists)

    def test_in_operator_nonexistent(self):
        root = Node()

        nonexistent_exists = 'nonexistent' in root

        self.assertFalse(nonexistent_exists)


if __name__ == '__main__':
    unittest.main()
