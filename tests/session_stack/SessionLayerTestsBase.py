import unittest

from contextshell.TreeRoot import TreeRoot
from contextshell.NodePath import NodePath
from contextshell.session_stack.SessionLayer import SessionLayer


class TestBases:
    class SessionLayerTestsBase(unittest.TestCase):
        def setUp(self):
            # TODO: cleanup when most layer tests will use this class
            self.existing_path = NodePath('.foo')
            self.missing_path = NodePath('.bar')

            self.tree = TreeRoot()

            self.session_stack = self.tree.create_session()
            self.session_stack.create(self.existing_path, 'foo')

            self.root = self.tree.root
            self.existing_node = self.root[self.existing_path.base_name]

            self.session_stack.push(self.prepare_layer(self.session_stack))
            self.layer = self.session_stack.top

        def prepare_layer(self, session: SessionLayer) -> SessionLayer:
            raise NotImplementedError()

        def test_create(self):
            self.layer.create(self.missing_path)
            self.assertTrue(self.root.contains(self.missing_path.base_name))
            bar_node = self.root[self.missing_path.base_name]
            self.assertIsNone(bar_node.get())

        def test_create_value(self):
            self.layer.create(self.missing_path, 123)
            bar_node = self.root[self.missing_path.base_name]
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
            self.assertFalse(self.root.contains(self.existing_path.base_name))

        def test_remove_nonexistent(self):
            with self.assertRaises(NameError):
                self.layer.remove(self.missing_path)

        def test_remove_root(self):
            with self.assertRaises(NameError):
                self.layer.remove(NodePath('.'))

        def test_list(self):
            list_result = self.layer.list(NodePath('.'))
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
