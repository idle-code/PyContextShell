import unittest

from contextshell.session_stack.PathVirtualAttributeLayer import *
from contextshell.session_stack.SessionStack import *
from tests.session_stack.SessionLayerTestsBase import TestBases


class BasicPathVirtualAttributeLayerTests(TestBases.SessionLayerTestsBase):
    def prepare_layer(self, session: SessionLayer) -> SessionLayer:
        return PathVirtualAttributeLayer()


class PathVirtualAttributeLayerTests(TestBases.LayerTestsBase):
    foo_path = NodePath('.foo')
    foo_path_path = NodePath.join(foo_path, '@path')

    def prepare_layer(self, session: SessionLayer) -> SessionLayer:
        session.create(self.foo_path, "foo")
        return PathVirtualAttributeLayer()

    def test_get_virtual(self):
        path_value = self.tested_layer.get(self.foo_path_path)
        self.assertEqual(NodePath('.foo'), path_value)

        path_value = self.tested_layer.get(NodePath('.@path'))
        self.assertEqual(NodePath('.'), path_value)

    def test_get_virtual_virtual(self):
        path_value = self.tested_layer.get(NodePath.join(self.foo_path_path, '@path'))
        self.assertEqual(NodePath('.foo.@path'), path_value)

    def test_set_virtual(self):
        with self.assertRaises(RuntimeError):
            self.tested_layer.set(self.foo_path_path, NodePath('.bar'))

    def test_remove_virtual(self):
        with self.assertRaises(RuntimeError):
            self.tested_layer.remove(self.foo_path_path)

    def test_list_virtual_parent(self):
        foo_nodes = self.tested_layer.list(self.foo_path)
        self.assertIn(self.foo_path_path, foo_nodes)

    def test_virtual_exists(self):
        self.assertTrue(self.tested_layer.exists(self.foo_path_path))

    def test_create_virtual(self):
        with self.assertRaises(RuntimeError):
            self.tested_layer.create(self.foo_path_path, 123)

    # TODO: check shadowing of existing attributes

if __name__ == '__main__':
    unittest.main()
