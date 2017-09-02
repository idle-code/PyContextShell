import unittest

from contextshell.Node import Node
from contextshell.session_stack.SessionLayer import *


class SessionLayerTestsBase(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.base_path = NodePath('.basic_tests')
        self.root.append(Node(), self.base_path.base_name)
        self.base_node = self.root[self.base_path.base_name]
        self.base_node.append(Node("foo"), "foo")

        self.existing_path = NodePath.join(self.base_path, 'foo')
        self.existing_node = self.base_node[self.existing_path.base_name]
        self.missing_path = NodePath.join(self.base_path, 'bar')

        self.layer = self.create_layer()

    def create_layer(self) -> SessionLayer:
        raise NotImplementedError()

    def test_create(self):
        self.layer.create(self.missing_path)
        self.assertTrue(self.base_node.contains(self.missing_path.base_name))
        bar_node = self.base_node[self.missing_path.base_name]
        self.assertIsNone(bar_node.get())

    def test_create_value(self):
        self.layer.create(self.missing_path, 123)
        bar_node = self.base_node[self.missing_path.base_name]
        self.assertEqual(123, bar_node.get())

    def test_create_existing(self):
        with self.assertRaises(NameError):
            self.layer.create(self.existing_path)

    def test_create_existing_value(self):
        with self.assertRaises(NameError):
            self.layer.create(self.existing_path, 321)

    def test_create_in_nonexistent_parent(self):
        with self.assertRaises(NameError):
            self.layer.create(NodePath.join(self.missing_path, 'spam'))

    def test_exists(self):
        self.assertTrue(self.layer.exists(self.existing_path))
        self.assertFalse(self.layer.exists(self.missing_path))

    def test_remove(self):
        self.layer.remove(self.existing_path)
        self.assertFalse(self.base_node.contains(self.existing_path.base_name))

    def test_remove_nonexistent(self):
        with self.assertRaises(NameError):
            self.layer.remove(self.missing_path)

    def test_remove_root(self):
        with self.assertRaises(NameError):
            self.layer.remove(NodePath('.'))

    def test_list(self):
        list_result = self.layer.list(self.base_path)
        self.assertIn(self.existing_path, list_result)

    def test_list_nonexistent(self):
        with self.assertRaises(NameError):
            self.layer.list(self.missing_path)

    def test_get(self):
        self.assertEqual("foo", self.layer.get(self.existing_path))

    def test_get_nonexistent(self):
        with self.assertRaises(NameError):
            self.layer.get(self.missing_path)

    def test_set(self):
        self.assertEqual("foo", self.existing_node.get())
        self.layer.set(self.existing_path, "FOO")
        self.assertEqual("FOO", self.existing_node.get())

    def test_set_nonexistent(self):
        with self.assertRaises(NameError):
            self.layer.set(self.missing_path, 332)

if __name__ == '__main__':
    unittest.main()
