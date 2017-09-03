import unittest

from contextshell.session_stack.RelativeLayer import *
from contextshell.session_stack.SessionStack import *
from contextshell.TreeRoot import TreeRoot
from tests.session_stack.SessionLayerTestsBase import TestBases


class BasicSessionLayerTests(TestBases.SessionLayerTestsBase):
    def prepare_layer(self, session: SessionLayer) -> SessionLayer:
        backing_path = NodePath('.current_path')
        start_path = NodePath('.foo')
        return RelativeLayer(backing_path, start_path)


@unittest.skip("Fix when VirtualNodeLayer will be available")
class RelativeLayerTests(unittest.TestCase):
    def setUp(self):
        root = TreeRoot()
        # Create backing and test nodes
        session = root.create_session()
        session.create(NodePath(".first"), 1)
        session.create(NodePath(".first.second"), 2)
        session.create(NodePath(".first.second.third"), 3)
        session.create(NodePath(".first.second.third.foo"), 'foo3')
        session.create(NodePath(".first.second.foo"), 'foo2')
        session.create(NodePath(".first.foo"), 'foo1')
        session.create(NodePath(".foo"), 'foo0')

        # Setup session stack (to push TemporarySession on top)
        self.storage_layer = root.create_session()
        session_stack = SessionStack(self.storage_layer)
        self.backing_path = NodePath('.current_path')
        session_stack.push(RelativeLayer(self.backing_path, NodePath('.first')))
        self.session = session_stack

    def test_current_path_exists(self):
        self.assertTrue(self.session.exists(self.backing_path))

    def test_get_current_path(self):
        current_path = self.session.get(self.backing_path)
        self.assertEqual(current_path, NodePath(".first"))

    def test_set_current_path(self):
        self.session.set(self.backing_path, NodePath('.'))
        current_path = self.session.get(self.backing_path)
        self.assertEqual(current_path, NodePath('.'))

    def test_set_current_path_relative(self):
        self.session.set(self.backing_path, NodePath('second'))
        current_path = self.session.get(self.backing_path)
        self.assertEqual(current_path, NodePath('second'))
        with self.assertRaises(NameError):
            self.session.get(NodePath('second'))

    def test_absolute_get(self):
        foo_value = self.session.get(NodePath('.first.second.foo'))
        self.assertEqual('foo2', foo_value)

    def test_relative_get(self):
        foo_value = self.session.get(NodePath('foo'))
        self.assertEqual('foo1', foo_value)

    def test_relative_get_after_change(self):
        self.session.set(self.backing_path, NodePath('.first.second.third'))
        current_path = self.session.get(self.backing_path)

        foo_value = self.session.get(NodePath('foo'))
        self.assertEqual('foo3', foo_value)

    def test_absolute_set(self):
        self.session.set(NodePath('.first.second.foo'), 'foobar')
        foo_value = self.storage_layer.get(NodePath('.first.second.foo'))
        self.assertEqual('foobar', foo_value)

    def test_relative_set(self):
        self.session.set(NodePath('second.foo'), 'foobar')
        foo_value = self.storage_layer.get(NodePath('.first.second.foo'))
        self.assertEqual('foobar', foo_value)

    def test_absolute_list(self):
        first_nodes = self.session.list(NodePath('.first'))
        expected_nodes = [NodePath('.first.second'),
                          NodePath('.first.foo')]
        self.assertListEqual(expected_nodes, first_nodes)

    def test_relative_list(self):
        second_nodes = self.session.list(NodePath('second'))
        expected_nodes = [NodePath('.first.second.third'),
                          NodePath('.first.second.foo')]
        self.assertListEqual(expected_nodes, second_nodes)

    def test_absolute_exists(self):
        self.assertTrue(self.session.exists(NodePath('.first.foo')))
        self.assertFalse(self.session.exists(NodePath('.first.bar')))

    def test_relative_exists(self):
        self.assertTrue(self.session.exists(NodePath('second')))
        self.assertFalse(self.session.exists(NodePath('second.bar')))

    def test_absolute_create(self):
        self.session.create(NodePath(".first.second.bar"), 'bar')
        self.assertEqual('bar', self.storage_layer.get(NodePath('.first.second.bar')))

    def test_relative_create(self):
        self.session.create(NodePath("second.bar"), 'bar')
        self.assertEqual('bar', self.storage_layer.get(NodePath('.first.second.bar')))

    def test_absolute_remove(self):
        self.session.remove(NodePath(".first.second.foo"))
        self.assertFalse(self.storage_layer.exists(NodePath('.first.second.foo')))

    def test_relative_remove(self):
        self.session.remove(NodePath("second.foo"))
        self.assertFalse(self.storage_layer.exists(NodePath('.first.second.foo')))


@unittest.skip("TODO next")
class RelativeLayerActionsTests(unittest.TestCase):
    def setUp(self):
        self.root = TreeRoot()
        self.session = TreeRoot.create_session()

    def test_cd(self):
        raise NotImplementedError()

    def test_pwd(self):
        raise NotImplementedError()


if __name__ == '__main__':
    unittest.main()
