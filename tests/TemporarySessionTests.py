import unittest

from TreeRoot import TreeRoot
from TemporarySession import *


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


if __name__ == '__main__':
    unittest.main()
