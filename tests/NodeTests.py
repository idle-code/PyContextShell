import unittest
from Node2 import Node


class NodeValueTests(unittest.TestCase):
    def test_new_node_have_no_value(self):
        empty_node = Node()
        self.assertEqual(None, empty_node.get())

    def test_get_value(self):
        int_node = Node(123)
        self.assertEqual(123, int_node.get())

        str_node = Node("spam")
        self.assertEqual("spam", str_node.get())

    def test_set_value(self):
        int_node = Node(123)
        self.assertEqual(123, int_node.get())
        int_node.set(321)
        self.assertEqual(321, int_node.get())

    def test_set_value_different_type(self):
        int_node = Node(123)
        self.assertIs(int, type(int_node.get()))
        with self.assertRaises(TypeError):
            int_node.set("string value")


class NodeSubnodesByNameTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.foo = Node(1)

    def test_new_node_have_no_subnodes(self):
        empty_node = Node()
        self.assertEqual(0, len(empty_node.list()))
        self.assertIsNone(self.root.parent)

    def test_append(self):
        self.root.append('foo', self.foo)
        self.root.append('bar', Node(2))

        self.assertEqual(2, len(self.root.list()))
        node_values = list(map(lambda n: self.root[n].get(), self.root.list()))
        self.assertListEqual([1, 2], node_values)
        self.assertIs(self.root, self.foo.parent)

    def test_append_none_name(self):
        with self.assertRaises(NameError):
            self.root.append(None, self.foo)

    def test_append_empty_name(self):
        with self.assertRaises(NameError):
            self.root.append('', self.foo)

    def test_append_none_node(self):
        with self.assertRaises(ValueError):
            self.root.append('foo', None)

    def test_append_existing(self):
        self.root.append('foo', self.foo)
        with self.assertRaises(NameError):
            self.root.append('foo', Node(2))

    def test_retrieve_by_name(self):
        self.root.append('foo', self.foo)
        self.assertIs(self.foo, self.root.get_node(name='foo'))

    def test_retrieve_by_getitem(self):
        self.root.append('foo', self.foo)
        self.assertIs(self.foo, self.root['foo'])

    def test_retrieve_nonexistent_name(self):
        self.assertIs(None, self.root.get_node(name='bar'))

    def test_retrieve_nonexistent_by_getitem(self):
        with self.assertRaises(KeyError):
            self.root['bar']

    def test_remove_by_name(self):
        self.root.append('foo', self.foo)
        a = self.root.remove(name='foo')
        self.assertEqual(0, len(self.root.list()))
        self.assertIs(self.foo, a)
    
    def test_remove_nonexistent_name(self):
        with self.assertRaises(NameError):
            self.root.remove(name='bar')

    def test_exists_name(self):
        self.root.append('foo', self.foo)
        self.assertTrue(self.root.contains(name='foo'))
        self.assertFalse(self.root.contains(name='bar'))

    # def test_exists_by_in(self):
    #     self.root.append('foo', self.foo)
    #     self.assertTrue('foo' in self.root)
    #     self.assertFalse('bar' in self.root)

if __name__ == '__main__':
    unittest.main()
