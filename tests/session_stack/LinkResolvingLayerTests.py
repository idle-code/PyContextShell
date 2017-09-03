import unittest

from contextshell.session_stack.LinkResolvingLayer import *
from contextshell.session_stack.SessionStack import *
from tests.session_stack.TestBases import TestBases


class BasicLinkResolvingLayerTests(TestBases.SessionLayerTestsBase):
    def prepare_layer(self, session: SessionLayer) -> SessionLayer:
        return LinkResolvingLayer()


class LinkResolvingLayerTests(TestBases.LayerTestsBase):
    link_path = NodePath('.link')
    link_foo_path = NodePath('.link.foo')
    backing_path = NodePath('.backing_node')
    backing_foo_path = NodePath('.backing_node.foo')

    def prepare_layer(self, session: SessionLayer) -> SessionLayer:
        session.create(self.backing_path, "backing")
        session.create(self.backing_foo_path, "foo")
        # TODO: create link by create.link action
        session.create(self.link_path, self.backing_path)  # Creates absolute link
        return LinkResolvingLayer()

    def test_get(self):
        link_value = self.tested_layer.get(self.link_path)
        self.assertEqual("backing", link_value)

    def test_get_under_link(self):
        foo_value = self.tested_layer.get(self.link_foo_path)
        self.assertEqual("foo", foo_value)

    def test_set(self):
        self.tested_layer.set(self.link_path, "backing_from_link")
        backing_value = self.storage_layer.get(self.backing_path)
        self.assertEqual("backing_from_link", backing_value)

    def test_remove_link(self):
        self.tested_layer.remove(self.link_path)
        self.assertFalse(self.tested_layer.exists(self.link_path))
        self.assertTrue(self.tested_layer.exists(self.backing_path))

    def test_remove_under_link(self):
        self.tested_layer.remove(self.link_foo_path)
        self.assertFalse(self.tested_layer.exists(self.link_foo_path))
        self.assertFalse(self.storage_layer.exists(self.backing_foo_path))

    def test_remove_backing(self):
        self.tested_layer.remove(self.backing_path)
        self.assertTrue(self.tested_layer.exists(self.link_path))
        self.assertFalse(self.tested_layer.exists(self.backing_path))

    def test_invalid_link(self):
        self.storage_layer.remove(self.backing_path)
        with self.assertRaises(NameError):
            self.tested_layer.get(self.link_path)

    def test_list(self):
        link_list = self.tested_layer.list(self.link_path)
        self.assertListEqual([NodePath(".link.foo")], link_list)

    def test_exists(self):
        self.assertTrue(self.tested_layer.exists(self.link_foo_path))

    def test_create(self):
        link_bar_path = NodePath.join(self.link_path, 'bar')
        backing_bar_path = NodePath.join(self.backing_path, 'bar')
        self.tested_layer.create(link_bar_path, 'bar')
        self.assertEqual('bar', self.tested_layer.get(link_bar_path))
        self.assertEqual('bar', self.tested_layer.get(backing_bar_path))
        self.assertEqual('bar', self.storage_layer.get(backing_bar_path))


@unittest.skip("TODO: when session actions will be available")
class LinkResolvingLayerActionsTests(unittest.TestCase):
    @unittest.skip("Write when create.link action will be available")
    def test_create_link(self):
        raise NotImplementedError()

    @unittest.skip("Implement when action for reading link content will be available")
    def test_read_link(self):
        raise NotImplementedError()


if __name__ == '__main__':
    unittest.main()
