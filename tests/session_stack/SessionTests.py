import unittest

from contextshell.Node import Node
from contextshell.NodePath import NodePath
from contextshell.ActionNode import ActionNode
from contextshell.session_stack.Session import Session
from contextshell.session_stack.CrudSessionLayer import CrudSessionLayer
from contextshell.session_stack.StorageLayer import StorageLayer
from tests.session_stack.TestBases import TestBases


class FakeSessionAction(ActionNode):
    path = NodePath('fake.path')
    def __init__(self):
        super().__init__(self.path, lambda *args: None)


class FakeCrudSessionLayer(CrudSessionLayer):
    @property
    def session_actions(self):
        return [FakeSessionAction()]


class SessionTests(unittest.TestCase):
    def setUp(self):
        root = Node()

        self.session = Session(StorageLayer(root))
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

    def test_uninstall_action_none(self):
        with self.assertRaises(ValueError):
            self.session.uninstall_action(None)

    def test_install_action(self):
        action = ActionNode('act', lambda x: x)

        self.session.install_action(action)

        self.assertTrue(self.session.exists('.@actions.act'))

    def test_uninstall_action(self):
        action = ActionNode('act', lambda x: x)
        self.session.install_action(action)

        self.session.uninstall_action(action.path)

        self.assertFalse(self.session.exists('.@actions.act'))

    def test_install_action_nested(self):
        action = ActionNode('foo.bar', lambda x: x)

        self.session.install_action(action)

        self.assertTrue(self.session.exists('.@actions.foo.bar'))

    def test_uninstall_action_nested(self):
        action = ActionNode('foo.bar', lambda x: x)
        self.session.install_action(action)

        self.session.uninstall_action(action.path)

        self.assertFalse(self.session.exists('.@actions.foo.bar'))

    def test_install_action_in_path(self):
        action = ActionNode('foo.bar', lambda x: x)

        self.session.install_action(action, NodePath('.foo'))

        self.assertTrue(self.session.exists('.foo.@actions.foo.bar'))

    def test_uninstall_action_from_path(self):
        action = ActionNode('foo.bar', lambda x: x)
        self.session.install_action(action, NodePath('.foo'))

        self.session.uninstall_action(action.path, NodePath('.foo'))

        self.assertFalse(self.session.exists('.foo.@actions.foo.bar'))

    def test_push_layer_installs_action(self):
        from contextshell.session_stack.SessionStorageLayer import SessionStorageLayer
        layer = FakeCrudSessionLayer()

        self.session.push(layer)

        action_path = NodePath.join(SessionStorageLayer.session_path, Session.actions_branch_name, FakeSessionAction.path)
        self.assertTrue(self.session.exists(action_path))

    def test_pop_layer_uninstall_action(self):
        from contextshell.session_stack.SessionStorageLayer import SessionStorageLayer
        layer = FakeCrudSessionLayer()
        self.session.push(layer)
        action_path = NodePath.join(SessionStorageLayer.session_path, Session.actions_branch_name,
                                    FakeSessionAction.path)

        poped_layer = self.session.pop()

        self.assertIs(poped_layer, layer)
        self.assertFalse(self.session.exists(action_path))


if __name__ == '__main__':
    unittest.main()
