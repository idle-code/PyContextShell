import unittest

from TemporarySession import *
from contextshell.TreeRoot import TreeRoot


class TemporarySessionTests(unittest.TestCase):
    def setUp(self):
        self.path = NodePath('.temp')
        self.session = TemporarySession(TreeRoot(), self.path)

    def test_start(self):
        self.assertTrue(self.session.exists(self.path))
        root_nodes = self.session.list('.')
        self.assertTrue(self.path[0] in root_nodes)

    def test_node_create(self):
        foo_path = NodePath.join(self.path, 'foo')
        self.assertFalse(self.session.exists(foo_path))
        self.session.create(foo_path, 123)
        self.assertTrue(self.session.exists(foo_path))

    def test_finish(self):
        self.assertTrue(self.session.exists(self.path))
        self.session.finish()
        self.assertFalse(self.session.exists(self.path))


class TemporaryStorageSessionTests(unittest.TestCase):
    def setUp(self):
        self.path = NodePath('.temp')
        self.base = TreeRoot()
        self.base.create('.existing')
        self.first = TemporarySession(self.base, self.path)
        self.second = TemporarySession(self.base, self.path)

    def test_existing_path(self):
        pass  # TODO: how this session should behave?
        self.assertTrue(self.base.exists('.existing'))
        session = TemporarySession(self.base, '.existing')

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
