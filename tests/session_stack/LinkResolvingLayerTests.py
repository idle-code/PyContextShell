import unittest

from contextshell.session_stack.LinkResolvingLayer import *
from contextshell.session_stack.SessionStack import *
from contextshell.TreeRoot import TreeRoot


class LinkResolvingLayerTests(unittest.TestCase):
    def setUp(self):
        self.link_path = NodePath('.link')
        self.link_foo_path = NodePath('.link.foo')
        self.backing_path = NodePath('.backing_node')
        self.backing_foo_path = NodePath('.backing_node.foo')

        root = TreeRoot()
        # Create backing and test nodes
        session = root.create_session()
        session.create(self.backing_path, "backing")
        session.create(self.backing_foo_path, "foo")
        # TODO: create link by create.link action
        session.create(self.link_path, self.backing_path)  # Creates absolute link
        self.assertTrue(session.exists(self.backing_path))
        self.assertTrue(session.exists(self.link_path))

        # Setup session stack (to push TemporarySession on top)
        self.storage_layer = root.create_session()
        session_stack = SessionStack(self.storage_layer)
        session_stack.push(LinkResolvingLayer())
        self.session = session_stack

    def test_get(self):
        link_value = self.session.get(self.link_path)
        self.assertEqual("backing", link_value)

    def test_get_under_link(self):
        foo_value = self.session.get(self.link_foo_path)
        self.assertEqual("foo", foo_value)

    def test_set(self):
        self.session.set(self.link_path, "backing_from_link")
        backing_value = self.storage_layer.get(self.backing_path)
        self.assertEqual("backing_from_link", backing_value)

    def test_remove_link(self):
        self.session.remove(self.link_path)
        self.assertFalse(self.session.exists(self.link_path))
        self.assertTrue(self.session.exists(self.backing_path))

    def test_remove_under_link(self):
        self.session.remove(self.link_foo_path)
        self.assertFalse(self.session.exists(self.link_foo_path))
        self.assertFalse(self.storage_layer.exists(self.backing_foo_path))

    def test_remove_backing(self):
        self.session.remove(self.backing_path)
        self.assertTrue(self.session.exists(self.link_path))
        self.assertFalse(self.session.exists(self.backing_path))

    def test_invalid_link(self):
        self.storage_layer.remove(self.backing_path)
        with self.assertRaises(NameError):
            self.session.get(self.link_path)

    def test_list(self):
        link_list = self.session.list(self.link_path)
        self.assertListEqual([NodePath(".link.foo")], link_list)

    def test_exists(self):
        self.assertTrue(self.session.exists(self.link_foo_path))

    def test_create(self):
        link_bar_path = NodePath.join(self.link_path, 'bar')
        backing_bar_path = NodePath.join(self.backing_path, 'bar')
        self.session.create(link_bar_path, 'bar')
        self.assertEqual('bar', self.session.get(link_bar_path))
        self.assertEqual('bar', self.session.get(backing_bar_path))
        self.assertEqual('bar', self.storage_layer.get(backing_bar_path))


@unittest.skip
class LinkResolvingLayerActionsTests(unittest.TestCase):
    @unittest.skip("Write when create.link action will be available")
    def test_create_link(self):
        raise NotImplementedError()

    @unittest.skip("Implement when action for reading link content will be available")
    def test_read_link(self):
        raise NotImplementedError()


if __name__ == '__main__':
    unittest.main()
