import unittest
from Node2 import Node
from NodePath import NodePath

class NodeValueTests(unittest.TestCase):
    def test_new_node_have_no_value(self):
        empty_node = Node()
        self.assertEqual(None, empty_node.value)

    def test_get_value(self):
        int_node = Node(123)
        self.assertEqual(123, int_node.value)

        str_node = Node("spam")
        self.assertEqual("spam", str_node.value)

    def test_set_value(self):
        int_node = Node(123)
        self.assertEqual(123, int_node.value)
        int_node.value = 321
        self.assertEqual(321, int_node.value)

    def test_set_value_different_type(self):
        int_node = Node(123)
        self.assertIs(int, type(int_node.value))
        with self.assertRaises(TypeError):
            int_node.value = "string value"


class NodeSubnodesByNameTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.foo = Node(1)

    def test_new_node_have_no_subnodes(self):
        empty_node = Node()
        self.assertEqual(0, len(empty_node.subnodes))

    def test_append(self):
        self.root.append('foo', self.foo)
        self.root.append('bar', Node(2))
        self.assertEqual(2, len(self.root.subnodes))
        node_values = list(map(lambda n: n.value, self.root.subnodes))
        self.assertListEqual([1, 2], node_values)

    def test_append_none_name(self):
        with self.assertRaises(NameError):
            self.root.append(None, self.foo)

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

    def test_retrieve_nonexistent_name(self):
        self.assertIs(None, self.root.get_node(name='bar'))

    def test_remove_by_name(self):
        self.root.append('foo', self.foo)
        a = self.root.remove(name='foo')
        self.assertEqual(0, len(self.root.subnodes))
        self.assertIs(self.foo, a)
    
    def test_remove_nonexistent_name(self):
        with self.assertRaises(NameError):
            self.root.remove(name='bar')

    def test_exists_name(self):
        self.root.append('foo', self.foo)
        self.assertTrue(self.root.exists(name='foo'))
        self.assertFalse(self.root.exists(name='bar'))


class NodeSubnodesByPathTests(unittest.TestCase):
    # TODO: add tests for relative/absolute path access
    def setUp(self):
        self.root = Node()
        self.foo = Node(1)
        self.bar = Node(2)
        self.root.append('foo', self.foo)
        self.foo.append('bar', self.bar)

    def test_retrieve_by_path(self):
        bar = self.root.get_node(path='.foo.bar')
        self.assertIs(self.bar, bar)

        foo = self.root.get_node(path='.foo')
        self.assertIs(self.foo, foo)

        foobar_path = NodePath(['foo', 'bar'])
        bar = self.root.get_node(path=foobar_path)
        self.assertIs(self.bar, bar)

        root = self.root.get_node(path=NodePath())
        self.assertIs(self.root, root)

    def test_retrieve_nonexistent_path(self):
        self.assertIs(None, self.root.get_node(path='bar.spam'))

    def test_remove_by_path(self):
        self.assertEqual(1, len(self.foo.subnodes))
        bar = self.root.remove(path='foo.bar')
        self.assertEqual(0, len(self.foo.subnodes))
        self.assertIs(self.bar, bar)

    def test_remove_nonexistent_path(self):
        with self.assertRaises(NameError):
            self.root.remove(path='foo.spam')

    def test_remove_root(self):
        with self.assertRaises(NameError):
            self.root.remove(path=NodePath())

    def test_exists_path(self):
        self.assertTrue(self.root.exists(path='.foo.bar'))
        self.assertTrue(self.root.exists(path='foo.bar'))
        self.assertFalse(self.root.exists(path='.bar'))
        self.assertFalse(self.root.exists(path='bar'))
        self.assertFalse(self.root.exists(path='foo.bar.spam'))
        self.assertFalse(self.root.exists(path=NodePath(['foo', 'bar', 'baz'])))
        self.assertTrue(self.root.exists(path=NodePath()))

if __name__ == '__main__':
    unittest.main()
