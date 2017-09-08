import unittest

from contextshell.Node import Node
from contextshell.NodePath import NodePath
from contextshell.session_stack.SessionStack import SessionStack
from contextshell.session_stack.SessionManager import SessionManager
from contextshell.Command import Command
from contextshell.TreeRoot import TreeRoot
from contextshell.CommandInterpreter import CommandInterpreter
from contextshell.ActionNode import ActionNode


class SessionManagerTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.manager = SessionManager(self.root)

    def test_create_session(self):
        session = self.manager.create_session()

        self.assertIsInstance(session, SessionStack)
        session.create(NodePath('.foo'), 123)
        self.assertEqual(session.get(NodePath('.foo')), 123)

    def test_create_interpreter(self):
        interpreter = self.manager.create_interpreter()

        self.assertIsInstance(interpreter, CommandInterpreter)

    def test_relative_layer_session_action(self):
        interpreter = self.manager.create_interpreter()
        current_path = interpreter.execute(Command('pwd'))

        self.assertEqual(NodePath('.'), current_path)
