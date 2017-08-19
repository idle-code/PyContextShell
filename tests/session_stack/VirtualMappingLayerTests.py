import unittest

from contextshell.session_stack.VirtualMappingLayer import *
from contextshell.session_stack.SessionStack import *
from contextshell.TreeRoot import TreeRoot


class VirtualMappingLayerTests(unittest.TestCase):
    def setUp(self):
        self.virtual_path = NodePath('.virtual')
        self.backing_path = NodePath('.backing_node')

        root = TreeRoot()
        # Create backing node
        # TODO: move start to the constructor or use contextmanager
        session = root.create_session()
        session.start(None)
        session.create(self.backing_path)
        self.assertTrue(session.exists(self.backing_path))
        session.finish()

        # Setup session stack (to push TemporarySession on top)
        session_stack = SessionStack(root.create_session())
        session_stack.push(VirtualMappingLayer(self.virtual_path, self.backing_path))
        session_stack.start(None)
        self.assertTrue(session_stack.exists(self.virtual_path))
        self.assertIn(self.virtual_path, session_stack.list('.'))
        self.session = session_stack

    def tearDown(self):
        self.session.finish()
        # self.assertFalse(self.session.exists(self.virtual_path))

    def test_node_create(self):
        foo_path = NodePath.join(self.virtual_path, 'foo')
        self.assertFalse(self.session.exists(foo_path), "{} exists".format(foo_path))
        self.session.create(foo_path, 123)
        self.assertTrue(self.session.exists(foo_path), "{} doesn't exists".format(foo_path))


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
