import unittest

from contextshell.session_stack.PathVirtualAttributeLayer import *
from contextshell.session_stack.SessionStack import *
from contextshell.TreeRoot import TreeRoot


class PathVirtualAttributeLayerTests(unittest.TestCase):
    def setUp(self):
        self.foo_path = NodePath('.foo')
        self.foo_path_path = NodePath.join(self.foo_path, '@path')

        root = TreeRoot()
        # Create backing and test nodes
        session = root.create_session()
        session.create(self.foo_path, "foo")
        self.assertTrue(session.exists(self.foo_path))

        # Setup session stack (to push TemporarySession on top)
        self.storage_layer = root.create_session()
        session_stack = SessionStack(self.storage_layer)
        session_stack.push(PathVirtualAttributeLayer())
        self.session = session_stack

    def test_get(self):
        path_value = self.session.get(self.foo_path_path)
        self.assertEqual(NodePath('.foo'), path_value)

        path_value = self.session.get(NodePath('.@path'))
        self.assertEqual(NodePath('.'), path_value)

    def test_get_virtual(self):
        path_value = self.session.get(NodePath.join(self.foo_path_path, '@path'))
        self.assertEqual(NodePath('.foo.@path'), path_value)

    def test_set(self):
        with self.assertRaises(RuntimeError):
            self.session.set(self.foo_path_path, NodePath('.bar'))

    def test_remove(self):
        with self.assertRaises(RuntimeError):
            self.session.remove(self.foo_path_path)

    def test_list(self):
        foo_nodes = self.session.list(self.foo_path)
        self.assertListEqual([self.foo_path_path], foo_nodes)

    def test_exists(self):
        self.assertTrue(self.session.exists(self.foo_path_path))

    def test_create(self):
        with self.assertRaises(RuntimeError):
            self.session.create(self.foo_path_path, 123)

    # TODO: check shadowing of existing attributes

if __name__ == '__main__':
    unittest.main()
