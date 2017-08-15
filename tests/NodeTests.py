import unittest

from contextshell.Node import Node


class ValueTests(unittest.TestCase):
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


class SubnodesByNameTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.foo = Node(1)

    def test_new_node_have_no_subnodes(self):
        empty_node = Node()
        self.assertEqual(0, len(empty_node.list()))
        self.assertIsNone(self.root.parent)

    def test_append(self):
        self.root.append(self.foo, name='foo')
        self.root.append(Node(2), name='bar')

        self.assertEqual(2, len(self.root.list()))
        node_values = list(map(lambda n: self.root[n].get(), self.root.list()))
        self.assertListEqual([1, 2], node_values)
        self.assertIs(self.root, self.foo.parent)

    def test_append_empty_name(self):
        with self.assertRaises(NameError):
            self.root.append(self.foo, name='')

    def test_append_none_node(self):
        with self.assertRaises(ValueError):
            self.root.append(None, name='foo')

    def test_append_existing(self):
        self.root.append(self.foo, name='foo')
        with self.assertRaises(NameError):
            self.root.append(Node(2), 'foo')

    def test_retrieve_by_name(self):
        self.root.append(self.foo, name='foo')
        self.assertIs(self.foo, self.root.get_node(name='foo'))

    def test_retrieve_by_getitem(self):
        self.root.append(self.foo, name='foo')
        self.assertIs(self.foo, self.root['foo'])

    def test_retrieve_nonexistent_name(self):
        self.assertIs(None, self.root.get_node(name='bar'))

    def test_retrieve_nonexistent_by_getitem(self):
        with self.assertRaises(KeyError):
            self.root['bar']

    def test_remove_by_name(self):
        self.root.append(self.foo, name='foo')
        a = self.root.remove(name='foo')
        self.assertEqual(0, len(self.root.list()))
        self.assertIs(self.foo, a)
    
    def test_remove_nonexistent_name(self):
        with self.assertRaises(NameError):
            self.root.remove(name='bar')

    def test_exists_name(self):
        self.root.append(self.foo, name='foo')
        self.assertTrue(self.root.contains(name='foo'))
        self.assertFalse(self.root.contains(name='bar'))

    # def test_exists_by_in(self):
    #     self.root.append('foo', self.foo)
    #     self.assertTrue('foo' in self.root)
    #     self.assertFalse('bar' in self.root)


class SubnodesByIndexTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.first = Node(0)
        self.second = Node(1)

    def test_append_anonymous_none(self):
        with self.assertRaises(ValueError):
            self.root.append(None)

    def test_append(self):
        self.assertListEqual([], self.root.list())

        self.root.append(self.first)
        self.root.append(self.second)

        self.assertListEqual([0, 1], self.root.list())

        self.assertEqual(2, len(self.root.list()))
        self.assertIs(self.root, self.first.parent)
        self.assertIs(self.root, self.second.parent)

    def test_get_node_no_args(self):
        with self.assertRaises(NameError):
            self.root.get_node()

    def test_retrieve_by_index(self):
        self.root.append(self.first)
        self.root.append(self.second)
        self.assertIs(self.first, self.root.get_node(index=0))
        self.assertIs(self.second, self.root.get_node(index=1))

    def test_retrieve_by_getitem(self):
        self.root.append(self.first)
        self.root.append(self.second)
        self.assertIs(self.first, self.root[0])
        self.assertIs(self.second, self.root[1])

    def test_retrieve_nonexistent_index(self):
        self.assertIs(None, self.root.get_node(index=99))

    def test_retrieve_nonexistent_by_getitem(self):
        with self.assertRaises(KeyError):
            self.root[99]

    def test_remove_no_args(self):
        with self.assertRaises(NameError):
            self.root.remove()

    def test_remove_by_index(self):
        self.root.append(self.first)
        self.root.append(self.second)
        self.assertIs(self.first, self.root[0])
        self.assertListEqual([0, 1], self.root.list())

        first = self.root.remove(index=0)

        self.assertIs(self.first, first)
        self.assertListEqual([0], self.root.list())
        self.assertIs(self.second, self.root[0])

    def test_remove_nonexistent_index(self):
        with self.assertRaises(NameError):
            self.root.remove(index=99)

    def test_exists_no_args(self):
        with self.assertRaises(NameError):
            self.root.contains()

    def test_exists_index(self):
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
