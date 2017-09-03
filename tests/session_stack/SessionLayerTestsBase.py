import unittest

from contextshell.TreeRoot import TreeRoot
from contextshell.NodePath import NodePath
from contextshell.session_stack.SessionLayer import SessionLayer


class TestBases:
    class SessionLayerTestsBase(unittest.TestCase):
        def setUp(self):
            self.existing_path = NodePath('.foo')
            self.missing_path = NodePath('.bar')

            tree = TreeRoot()
            self.storage_layer = tree.create_session()
            self.storage_layer.create(self.existing_path, 'foo')

            self.tested_layer = tree.create_session()
            self.tested_layer.push(self.prepare_layer(self.tested_layer))

        def prepare_layer(self, session: SessionLayer) -> SessionLayer:
            raise NotImplementedError()

        def test_create(self):
            self.tested_layer.create(self.missing_path)

            self.assertTrue(self.storage_layer.exists(self.missing_path))
            bar_value = self.storage_layer.get(self.missing_path)
            self.assertIsNone(bar_value)

        def test_create_value(self):
            self.tested_layer.create(self.missing_path, 123)

            self.assertTrue(self.storage_layer.exists(self.missing_path))
            bar_value = self.storage_layer.get(self.missing_path)
            self.assertEqual(123, bar_value)

        def test_create_existing(self):
            with self.assertRaises(NameError):
                self.tested_layer.create(self.existing_path)

        def test_create_existing_value(self):
            with self.assertRaises(NameError):
                self.tested_layer.create(self.existing_path, 321)

        def test_create_in_nonexistent_parent(self):
            with self.assertRaises(NameError):
                self.tested_layer.create(NodePath.join(self.missing_path, 'spam'))

        def test_exists(self):
            self.assertTrue(self.tested_layer.exists(self.existing_path))
            self.assertFalse(self.tested_layer.exists(self.missing_path))

        def test_remove(self):
            self.tested_layer.remove(self.existing_path)
            self.assertFalse(self.storage_layer.exists(self.existing_path))

        def test_remove_nonexistent(self):
            with self.assertRaises(NameError):
                self.tested_layer.remove(self.missing_path)

        def test_remove_root(self):
            with self.assertRaises(NameError):
                self.tested_layer.remove(NodePath('.'))

        def test_list(self):
            list_result = self.tested_layer.list(NodePath('.'))
            self.assertIn(self.existing_path, list_result)

        def test_list_nonexistent(self):
            with self.assertRaises(NameError):
                self.tested_layer.list(self.missing_path)

        def test_get(self):
            self.assertEqual("foo", self.tested_layer.get(self.existing_path))

        def test_get_nonexistent(self):
            with self.assertRaises(NameError):
                self.tested_layer.get(self.missing_path)

        def test_set(self):
            existing_value = self.storage_layer.get(self.existing_path)
            self.assertEqual("foo", existing_value)

            self.tested_layer.set(self.existing_path, "FOO")

            existing_value = self.storage_layer.get(self.existing_path)
            self.assertEqual("FOO", existing_value)

        def test_set_nonexistent(self):
            with self.assertRaises(NameError):
                self.tested_layer.set(self.missing_path, 332)


if __name__ == '__main__':
    unittest.main()
