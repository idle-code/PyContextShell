from contextshell.Node import Node
from contextshell.NodePath import NodePath
from contextshell.session_stack.StorageLayer import StorageLayer
from contextshell.session_stack.SessionStack import SessionStack
from contextshell.session_stack.RelativeLayer import RelativeLayer
from contextshell.CommandInterpreter import CommandInterpreter


class SessionManager:
    def __init__(self, root: Node):
        self.root = root

    def create_session(self) -> SessionStack:
        stack = SessionStack(StorageLayer(self.root))
        stack.push(RelativeLayer(NodePath('.')))
        return stack

    def create_interpreter(self) -> CommandInterpreter:
        return CommandInterpreter(self.create_session())
