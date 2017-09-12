import unittest

from contextshell.Node import Node
from contextshell.NodePath import NodePath
from contextshell.ActionNode import ActionNode
from contextshell.session_stack.SessionManager import SessionManager
from contextshell.session_stack.SessionLayer import SessionLayer
from tests.session_stack.TestBases import TestBases


class BasicSessionTests(TestBases.SessionLayerTestsBase):
    def prepare_layer(self, session: SessionLayer) -> SessionLayer:
        root = Node()
        manager = SessionManager(root)

        return manager.create_session()


class SessionTests(unittest.TestCase):
    def setUp(self):
        root = Node()
        manager = SessionManager(root)
        self.session = manager.create_session()
        self.session.create(NodePath('.foo'))

    def test_create_partially_present_path(self):
        path_to_create = NodePath('.foo.bar.spam')
        self.assertTrue(self.session.exists(NodePath('.foo')))
        self.assertFalse(self.session.exists(NodePath('.foo.bar')))

        self.session.create_path(path_to_create)

        self.assertTrue(self.session.exists(path_to_create))

    def test_create_path(self):
        path_to_create = NodePath('.bar.spam.foo')
        self.assertFalse(self.session.exists(NodePath('.bar')))

        self.session.create_path(path_to_create)

        self.assertTrue(self.session.exists(path_to_create))

    def test_install_action_none(self):
        with self.assertRaises(ValueError):
            self.session.install_action(None)

    def test_install_action(self):
        action = ActionNode('act', lambda x: x)
        self.session.install_action(action)
        self.assertTrue(self.session.exists('.@actions.act'))

    def test_install_action_nested(self):
        action = ActionNode('foo.bar', lambda x: x)
        self.session.install_action(action)
        self.assertTrue(self.session.exists('.@actions.foo.bar'))

    def test_install_action_in_path(self):
        action = ActionNode('foo.bar', lambda x: x)
        self.session.install_action(action, 'foo')
        self.assertTrue(self.session.exists('.foo.@actions.foo.bar'))

if __name__ == '__main__':
    unittest.main()
