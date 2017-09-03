import unittest

from contextshell.session_stack.RelativeLayer import *
from contextshell.session_stack.SessionStack import *
from tests.session_stack.TestBases import TestBases


class BasicSessionLayerTests(TestBases.SessionLayerTestsBase):
    backing_path = NodePath('.current_path')
    start_path = NodePath('.foo')

    def prepare_layer(self, session: SessionLayer) -> SessionLayer:
        return RelativeLayer(self.backing_path, self.start_path)


class RelativeLayerTests(TestBases.LayerTestsBase):
    current_path = NodePath('.current_path')

    def prepare_layer(self, session: SessionLayer) -> SessionLayer:
        session.create(NodePath(".first"), 1)
        session.create(NodePath(".first.second"), 2)
        session.create(NodePath(".first.second.third"), 3)
        session.create(NodePath(".first.second.third.foo"), 'foo3')
        session.create(NodePath(".first.second.foo"), 'foo2')
        session.create(NodePath(".first.foo"), 'foo1')
        session.create(NodePath(".foo"), 'foo0')

        return RelativeLayer(self.current_path, NodePath('.first'))

    def test_current_path_exists(self):
        self.assertTrue(self.tested_layer.exists(self.current_path))

    def test_get_current_path(self):
        current_path = self.tested_layer.get(self.current_path)
        self.assertEqual(current_path, NodePath(".first"))

    def test_set_current_path(self):
        self.tested_layer.set(self.current_path, NodePath('.'))
        current_path = self.tested_layer.get(self.current_path)
        self.assertEqual(current_path, NodePath('.'))

    def test_set_current_path_bad_type(self):
        with self.assertRaises(ValueError):
            self.tested_layer.set(self.current_path, 3.14)

    def test_set_current_path_relative(self):
        self.tested_layer.set(self.current_path, NodePath('second'))
        current_path = self.tested_layer.get(self.current_path)
        self.assertEqual(current_path, NodePath('.first.second'))
        self.assertTrue(self.tested_layer.exists(NodePath('third')))

    def test_set_current_path_nonexistent(self):
        with self.assertRaises(ValueError):
            self.tested_layer.set(self.current_path, NodePath('relative'))
        with self.assertRaises(ValueError):
            self.tested_layer.set(self.current_path, NodePath('.absolute'))

    def test_relative_get(self):
        foo_value = self.tested_layer.get(NodePath('foo'))
        self.assertEqual('foo1', foo_value)

    def test_relative_get_after_change(self):
        self.tested_layer.set(self.current_path, NodePath('.first.second.third'))
        foo_value = self.tested_layer.get(NodePath('foo'))
        self.assertEqual('foo3', foo_value)

    def test_relative_set(self):
        self.tested_layer.set(NodePath('second.foo'), 'foobar')
        foo_value = self.storage_layer.get(NodePath('.first.second.foo'))
        self.assertEqual('foobar', foo_value)

    def test_relative_list(self):
        second_nodes = self.tested_layer.list(NodePath('second'))
        expected_nodes = [NodePath('.first.second.third'),
                          NodePath('.first.second.foo')]
        self.assertListEqual(expected_nodes, second_nodes)

    def test_relative_exists(self):
        self.assertTrue(self.tested_layer.exists(NodePath('second')))
        self.assertFalse(self.tested_layer.exists(NodePath('second.bar')))

    def test_relative_create(self):
        self.tested_layer.create(NodePath("second.bar"), 'bar')
        self.assertEqual('bar', self.storage_layer.get(NodePath('.first.second.bar')))

    def test_relative_remove(self):
        self.tested_layer.remove(NodePath("second.foo"))
        self.assertFalse(self.storage_layer.exists(NodePath('.first.second.foo')))


@unittest.skip("TODO next")
class RelativeLayerActionsTests(unittest.TestCase):
    def test_cd(self):
        raise NotImplementedError()

    def test_pwd(self):
        raise NotImplementedError()


if __name__ == '__main__':
    unittest.main()
