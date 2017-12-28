import unittest

from contextshell.Node import Node


class ValueTests(unittest.TestCase):
    def test_new_node_have_no_value(self):
        empty_node = Node()

        self.assertEqual(None, empty_node.get())

    def test_constructor_sets_value(self):
        int_node = Node(123)

        self.assertEqual(123, int_node.get())

    def test_set_value(self):
        int_node = Node(123)

        int_node.set(321)

        self.assertEqual(321, int_node.get())

    def test_set_value_different_type(self):
        int_node = Node(123)

        with self.assertRaises(TypeError):
            int_node.set("string value")


class SubnodesByNameTests(unittest.TestCase):
    def test_new_node_have_no_subnodes(self):
        empty_node = Node()

        self.assertEqual(0, len(empty_node.list()))

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

    def test_retrieve_by_name(self):
        root = Node()
        foo = Node()
        root.append(foo, name='foo')

        retrieved_foo_node = root.get_node(name='foo')

        self.assertIs(foo, retrieved_foo_node)

    def test_retrieve_by_getitem(self):
        root = Node()
        foo = Node()
        root.append(foo, name='foo')

        retrieved_foo_node = root['foo']

        self.assertIs(foo, retrieved_foo_node)

    def test_retrieve_nonexistent_by_name(self):
        root = Node()

        retrieved_foo_node = root.get_node(name='nonexistent')

        self.assertIs(None, retrieved_foo_node)

    def test_retrieve_nonexistent_by_getitem(self):
        root = Node()

        with self.assertRaises(KeyError):
            root['nonexistent']

    def test_remove_removes_name(self):
        root = Node()
        root.append(Node(), name='foo')

        root.remove(name='foo')

        self.assertEqual(0, len(root.list()))

    def test_remove_returns_node(self):
        root = Node()
        foo = Node()
        root.append(foo, name='foo')

        removed_node = root.remove(name='foo')

        self.assertIs(foo, removed_node)

    def test_remove_nonexistent_name(self):
        root = Node()

        with self.assertRaises(NameError):
            root.remove(name='nonexistent')

    def test_exists_existing(self):
        root = Node()
        root.append(Node(), name='foo')

        foo_exists = root.contains(name='foo')

        self.assertTrue(foo_exists)

    def test_exists_nonexistent(self):
        root = Node()

        nonexistent_exists = root.contains(name='nonexistent')

        self.assertFalse(nonexistent_exists)

    def test_in_operator_existing(self):
        root = Node()
        root.append(Node(), name='foo')

        foo_exists = 'foo' in root

        self.assertTrue(foo_exists)

    def test_in_operator_nonexistent(self):
        root = Node()

        nonexistent_exists = 'nonexistent' in root

        self.assertFalse(nonexistent_exists)


class SubnodesByIndexTests(unittest.TestCase):
    def test_append_anonymous_none(self):
        root = Node()

        with self.assertRaises(ValueError):
            root.append(None)

    def test_get_node_no_args(self):
        root = Node()

        with self.assertRaises(NameError):
            root.get_node()

    def test_retrieve_by_index(self):
        root = Node()

        self.root.append(self.first)
        self.root.append(self.second)
        self.assertIs(self.first, self.root.get_node(index=0))
        self.assertIs(self.second, self.root.get_node(index=1))

    def test_retrieve_by_getitem(self):
        root = Node()
        self.root.append(self.first)
        self.root.append(self.second)
        self.assertIs(self.first, self.root[0])
        self.assertIs(self.second, self.root[1])

    def test_retrieve_nonexistent_index(self):
        root = Node()
        self.assertIs(None, self.root.get_node(index=99))

    def test_retrieve_nonexistent_by_getitem(self):
        root = Node()
        with self.assertRaises(KeyError):
            self.root[99]

    def test_remove_no_args(self):
        root = Node()
        with self.assertRaises(NameError):
            self.root.remove()

    def test_remove_by_index(self):
        root = Node()
        self.root.append(self.first)
        self.root.append(self.second)
        self.assertIs(self.first, self.root[0])
        self.assertListEqual([0, 1], self.root.list())

        first = self.root.remove(index=0)

        self.assertIs(self.first, first)
        self.assertListEqual([0], self.root.list())
        self.assertIs(self.second, self.root[0])

    def test_remove_nonexistent_index(self):
        root = Node()
        with self.assertRaises(NameError):
            self.root.remove(index=99)

    def test_exists_no_args(self):
        root = Node()
        with self.assertRaises(NameError):
            self.root.contains()

    def test_exists_index(self):
        root = Node()
        self.root.append(self.first)
        self.assertTrue(self.root.contains(index=0))
        self.assertFalse(self.root.contains(index=1))
        self.assertFalse(self.root.contains(index=-1))

    # def test_exists_by_index(self):
    #     self.root.append('foo', self.foo)
    #     self.assertTrue('foo' in self.root)
    #     self.assertFalse('bar' in self.root)

if __name__ == '__main__':
    unittest.main()
