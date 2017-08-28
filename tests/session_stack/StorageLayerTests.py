import unittest

from contextshell.NodePath import NodePath
from contextshell.Node import Node
from contextshell.session_stack.StorageLayer import StorageLayer


class StorageLayerTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.root.append(Node("foo"), "foo")
        self.root.append(Node(123), "bar")
        self.storage_layer = StorageLayer(self.root)

    def test_resolve_absolute(self):
        foo_node = self.storage_layer.resolve(NodePath('.foo'))
        self.assertIs(foo_node, self.root['foo'])

    def test_resolve_relative(self):
        with self.assertRaises(NameError):
            self.storage_layer.resolve(NodePath('foo'))

    def test_create(self):
        self.storage_layer.create('.spam')
        self.assertTrue(self.root.contains('spam'))
        self.assertIsNone(self.root['spam'].get())

    def test_nested(self):
        self.storage_layer.create('.foo.spam')
        self.assertTrue(self.root['foo'].contains('spam'))

    def test_create_value(self):
        self.storage_layer.create('.spam', "SPAM")
        self.assertTrue(self.root.contains('spam'))
        self.assertEqual("SPAM", self.root['spam'].get())

    def test_create_existing(self):
        with self.assertRaises(NameError):
            self.storage_layer.create('.foo')

    def test_create_in_nonexistent_parent(self):
        with self.assertRaises(NameError):
            self.storage_layer.create('.spam.zoo')

    def test_exists(self):
        self.assertFalse(self.storage_layer.exists('.baz'))
        self.storage_layer.create('.baz')
        self.assertTrue(self.storage_layer.exists('.baz'))

    def test_remove(self):
        self.assertTrue(self.storage_layer.exists('.foo'))
        self.storage_layer.remove('.foo')
        self.assertFalse(self.storage_layer.exists('.foo'))

    def test_remove_nonexistent(self):
        with self.assertRaises(NameError):
            self.storage_layer.remove('.unknown.path')

    def test_remove_root(self):
        with self.assertRaises(NameError):
            self.storage_layer.remove('.')

    def test_list(self):
        root_elements = self.storage_layer.list('.')
        self.assertListEqual([NodePath('.foo'), NodePath('.bar')], root_elements)

    def test_list_empty(self):
        self.assertListEqual([], self.storage_layer.list('.foo'))

    def test_list_nonexistent(self):
        with self.assertRaises(NameError):
            self.storage_layer.list('.rabarbar')

    def test_get(self):
        self.assertEqual("foo", self.storage_layer.get('.foo'))
        self.assertEqual(123, self.storage_layer.get('.bar'))

    def test_get_nonexistent(self):
        with self.assertRaises(NameError):
            self.storage_layer.get('.spam')

    def test_set(self):
        self.assertEqual("foo", self.root['foo'].get())
        self.storage_layer.set('.foo', "FOO")
        self.assertEqual("FOO", self.root['foo'].get())

        self.assertEqual(123, self.root['bar'].get())
        self.storage_layer.set('.bar', 321)
        self.assertEqual(321, self.root['bar'].get())

    def test_set_nonexistent(self):
        with self.assertRaises(NameError):
            self.storage_layer.set('.spam', 332)

if __name__ == '__main__':
    unittest.main()
