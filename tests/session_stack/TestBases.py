import unittest

from contextshell.CommandInterpreter import CommandInterpreter
from contextshell.Node import Node
from contextshell.NodePath import NodePath
from contextshell.session_stack.CrudSessionLayer import CrudSessionLayer
from contextshell.session_stack.Session import Session
from contextshell.session_stack.StorageLayer import StorageLayer


class TestBases:
    class LayerTestsBase(unittest.TestCase):
        def setUp(self):
            root = Node()
            self.storage_layer = StorageLayer(root)
            self.session = Session(self.storage_layer)

            self.tested_layer = self.prepare_layer(self.session)
            self.session.push(self.tested_layer)

        def prepare_layer(self, session: CrudSessionLayer) -> CrudSessionLayer:
            raise NotImplementedError()

    class LayerActionsTestsBase(LayerTestsBase):
        def setUp(self):
            super().setUp()
            # TODO: install session actions
            # TODO: use SessionManager or explicit installation
            self.interpreter = CommandInterpreter(self.session)

    class SessionLayerTestsBase(LayerTestsBase):
        def setUp(self):
            super().setUp()
            self.existing_path = NodePath('.foo')
            self.missing_path = NodePath('.bar')

            self.storage_layer.create(self.existing_path, 'foo')
            self.assertTrue(self.storage_layer.exists(self.existing_path))

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

        def test_get_session_actions(self):
            from contextshell.ActionNode import ActionNode
            for action in self.tested_layer.session_actions:
                self.assertIsInstance(action, ActionNode)


if __name__ == '__main__':
    unittest.main()
