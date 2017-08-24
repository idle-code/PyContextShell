import unittest

from contextshell.session_stack.RelativeLayer import *
from contextshell.session_stack.SessionStack import *
from contextshell.TreeRoot import TreeRoot


class RelativeLayerTests(unittest.TestCase):
    def setUp(self):
        root = TreeRoot()
        # Create backing and test nodes
        session = root.create_session()
        session.start(None)  # TODO: move start to the constructor or use contextmanager
        session.create(NodePath(".first"), 1)
        session.create(NodePath(".first.second"), 2)
        session.create(NodePath(".first.second.third"), 3)
        session.create(NodePath(".first.second.third.foo"), 'foo3')
        session.create(NodePath(".first.second.foo"), 'foo2')
        session.create(NodePath(".first.foo"), 'foo1')
        session.create(NodePath(".foo"), 'foo0')
        session.finish()

        # Setup session stack (to push TemporarySession on top)
        self.storage_layer = root.create_session()
        session_stack = SessionStack(self.storage_layer)
        session_stack.push(RelativeLayer(NodePath('.')))
        self.session = session_stack
        self.session.start(None)

    def tearDown(self):
        self.session.finish()

    def test_current_path(self):
        raise NotImplementedError()

    def test_absolute_get(self):
        raise NotImplementedError()

    def test_relative_get(self):
        raise NotImplementedError()

    def test_relative_arguments(self):
        """Check if action arguments are rewritten as well"""
        raise NotImplementedError()


if __name__ == '__main__':
    unittest.main()
