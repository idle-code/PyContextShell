import unittest

from contextshell.session_stack.VirtualNodeLayer import *
from contextshell.session_stack.SessionStack import *
from tests.session_stack.TestBases import TestBases


class TestedVirtualNodeLayer(VirtualNodeLayer):
    def __init__(self):
        super().__init__(NodePath('.virtual'))
        self.value = 23

    def on_get(self):
        return self.value

    def on_set(self, new_value):
        self.value *= new_value


class BasicVirtualNodeLayerTests(TestBases.SessionLayerTestsBase):
    def prepare_layer(self, session: SessionLayer) -> SessionLayer:
        return TestedVirtualNodeLayer()


class VirtualNodeLayerTests(TestBases.LayerTestsBase):
    def prepare_layer(self, storage_layer: SessionLayer) -> SessionLayer:
        return TestedVirtualNodeLayer()

    def test_on_get(self):
        virtual_value = self.tested_layer.get(self.tested_layer.virtual_path)
        self.assertEqual(23, virtual_value)

    def test_on_set(self):
        self.tested_layer.set(self.tested_layer.virtual_path, 3)
        virtual_value = self.tested_layer.get(self.tested_layer.virtual_path)
        self.assertEqual(23 * 3, virtual_value)

    def test_virtual_exists(self):
        self.assertTrue(self.tested_layer.exists(self.tested_layer.virtual_path))

    def test_remove_virtual(self):
        with self.assertRaises(RuntimeError):
            self.tested_layer.remove(self.tested_layer.virtual_path)

    def test_create_under_virtual(self):
        with self.assertRaises(RuntimeError):
            foo_path = NodePath.join(self.tested_layer.virtual_path, 'foo')
            self.tested_layer.create(foo_path, 123)

    def test_list_parent(self):
        parent_paths = self.tested_layer.list(self.tested_layer.virtual_path.base_path)
        self.assertIn(self.tested_layer.virtual_path, parent_paths)

    def test_list_virtual(self):
        self.tested_layer.list(self.tested_layer.virtual_path)


if __name__ == '__main__':
    unittest.main()
