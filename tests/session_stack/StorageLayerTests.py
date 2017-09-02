import unittest

from contextshell.NodePath import NodePath
from contextshell.Node import Node
from contextshell.session_stack.StorageLayer import StorageLayer
from tests.session_stack.SessionLayerTestsBase import SessionLayerTestsBase


class StorageLayerTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.root.append(Node("foo"), "foo")
        self.root.append(Node(123), "bar")
        self.layer = StorageLayer(self.root)

    def test_resolve_absolute(self):
        foo_node = self.layer.resolve(NodePath('.foo'))
        self.assertIs(foo_node, self.root['foo'])

    def test_resolve_relative(self):
        with self.assertRaises(NameError):
            self.layer.resolve(NodePath('foo'))


class BasicStorageLayerTests(SessionLayerTestsBase):
    def create_layer(self) -> StorageLayer:
        return StorageLayer(self.root)


if __name__ == '__main__':
    unittest.main()
