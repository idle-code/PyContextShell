import unittest

from contextshell.Node import Node
from contextshell.ActionNode import ActionNode
from contextshell.NodePath import NodePath
from contextshell.session_stack.Session import Session
from contextshell.session_stack.SessionStorageLayer import SessionStorageLayer
from contextshell.session_stack.SessionManager import SessionManager
from contextshell.Command import Command
from contextshell.CommandInterpreter import CommandInterpreter


class SessionManagerTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.manager = SessionManager(self.root)

    def test_create_session(self):
        session = self.manager.create_session()

        self.assertIsInstance(session, Session)
        session.create(NodePath('.foo'), 123)
        self.assertEqual(session.get(NodePath('.foo')), 123)

    def test_session_storage_layer_present(self):
        session = self.manager.create_session()

        self.assertTrue(session.exists(SessionStorageLayer.session_path))

    def test_relative_layer_session_action(self):
        session = self.manager.create_session()
        interpreter = CommandInterpreter(session)
        current_path = interpreter.execute(Command('pwd'))

        self.assertEqual(NodePath('.'), current_path)
