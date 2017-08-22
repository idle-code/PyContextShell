import unittest

from contextshell.session_stack.VirtualMappingLayer import *
from contextshell.session_stack.SessionStack import *
from contextshell.TreeRoot import TreeRoot


class VirtualMappingLayerTests(unittest.TestCase):
    def setUp(self):
        self.virtual_path = NodePath('.virtual')
        self.backing_path = NodePath('.backing_node')
        self.virtual_foo_path = NodePath.join(self.virtual_path, 'foo')
        self.backing_foo_path = NodePath.join(self.backing_path, 'foo')

        root = TreeRoot()
        # Create backing and test nodes
        session = root.create_session()
        session.start(None)  # TODO: move start to the constructor or use contextmanager
        session.create(self.backing_path)
        session.create(self.backing_foo_path, 123)
        self.assertTrue(session.exists(self.backing_path))
        self.assertTrue(session.exists(self.backing_foo_path))
        self.assertFalse(session.exists(self.virtual_foo_path))
        session.finish()

        # Setup session stack (to push TemporarySession on top)
        self.storage_layer = root.create_session()
        session_stack = SessionStack(self.storage_layer)
        session_stack.push(VirtualMappingLayer(self.virtual_path, self.backing_path))
        self.session = session_stack
        self.session.start(None)

    def tearDown(self):
        self.session.finish()

    def test_list_virtual_parent(self):
        self.assertIn(self.virtual_path, self.session.list(self.virtual_path.base_path))

    def test_list_returned_values_from_virtual(self):
        virtual_list = self.session.list(self.virtual_path)
        self.assertGreater(len(virtual_list), 0)
        for path in virtual_list:
            self.assertTrue(self.virtual_path.is_parent_of(path),
                            "{} is not under {}".format(path, self.virtual_path))

    def test_list_returned_values_from_backing(self):
        backing_list = self.session.list(self.backing_path)
        self.assertGreater(len(backing_list), 0)
        for path in backing_list:
            self.assertTrue(self.backing_path.is_parent_of(path),
                            "{} is not under {}".format(path, self.backing_path))

    def test_node_create(self):
        self.storage_layer.remove(self.backing_foo_path)

        self.session.create(self.virtual_foo_path, 123)
        self.assertTrue(self.session.exists(self.virtual_foo_path))
        self.assertTrue(self.storage_layer.exists(self.backing_foo_path))

    def test_node_remove(self):
        self.session.remove(self.virtual_foo_path)
        self.assertFalse(self.session.exists(self.virtual_foo_path))
        self.assertFalse(self.storage_layer.exists(self.backing_foo_path))

    def test_node_exists(self):
        self.assertTrue(self.session.exists(self.virtual_foo_path))
        self.storage_layer.remove(self.backing_foo_path)
        self.assertFalse(self.session.exists(self.virtual_foo_path))

    def test_node_get(self):
        backing_foo_val = self.storage_layer.get(self.backing_foo_path)
        virtual_foo_val = self.session.get(self.virtual_foo_path)
        self.assertEqual(backing_foo_val, virtual_foo_val)

    def test_node_set(self):
        self.session.set(self.virtual_foo_path, 321)
        backing_foo_val = self.storage_layer.get(self.backing_foo_path)
        virtual_foo_val = self.session.get(self.virtual_foo_path)
        self.assertEqual(backing_foo_val, 321)
        self.assertEqual(virtual_foo_val, 321)


class VirtualMappingLayerSessionSeparationTests(unittest.TestCase):
    def setUp(self):
        self.first_backing_path = NodePath('.backing_node.first')
        self.second_backing_path = NodePath('.backing_node.second')
        self.common_path = NodePath('.common')

        root = TreeRoot()
        # Create backing and test nodes
        session = root.create_session()
        session.start(None)  # TODO: move start to the constructor or use contextmanager
        session.create(self.first_backing_path.base_path)
        session.create(self.first_backing_path, "First")
        session.create(self.second_backing_path, "Second")
        self.assertTrue(session.exists(self.first_backing_path))
        self.assertTrue(session.exists(self.second_backing_path))
        session.finish()

        # Setup session stack (to push TemporarySession on top)
        self.storage_layer = root.create_session()
        self.first_session = self._create_session_stack(self.first_backing_path)
        self.second_session = self._create_session_stack(self.second_backing_path)

    def _create_session_stack(self, backing_path: NodePath) -> SessionLayer:
        session_stack = SessionStack(self.storage_layer)
        session_stack.push(VirtualMappingLayer(self.common_path, self.second_backing_path))
        session_stack.start(None)
        return session_stack


@unittest.skip
class TemporaryStorageSessionTests(unittest.TestCase):
    def setUp(self):
        self.path = NodePath('.temp')
        self.base = TreeRoot()
        self.base.create('.existing')
        self.first = VirtualMappingLayer(self.base, self.path)
        self.second = VirtualMappingLayer(self.base, self.path)

    def test_existing_path(self):
        pass  # TODO: how this session should behave?
        self.assertTrue(self.base.exists('.existing'))
        session = VirtualMappingLayer(self.base, '.existing')

    def test_virtual_node_exists(self):
        self.assertFalse(self.base.exists(self.path))
        self.assertTrue(self.first.exists(self.path))
        self.assertTrue(self.second.exists(self.path))

    def test_independent_create(self):
        node_path = NodePath.join(self.path, 'node')

        self.assertFalse(self.first.exists(node_path))
        self.assertFalse(self.second.exists(node_path))
        self.first.create(node_path, 123)
        self.assertTrue(self.first.exists(node_path))
        self.assertFalse(self.second.exists(node_path))

        self.second.create(node_path, 321)
        self.assertTrue(self.second.exists(node_path))

        self.assertEqual(123, self.first.get(node_path))
        self.assertEqual(321, self.second.get(node_path))


if __name__ == '__main__':
    unittest.main()
