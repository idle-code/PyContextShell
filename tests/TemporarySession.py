from Node import Node
from Session import *


class TemporarySession(Session):
    def __init__(self, underlying_session: Session, temp_path: NodePath):
        self.backend = underlying_session
        self.temp_path = temp_path
        self.temp_node = Node()
        self.start()

    def start(self):
        self.create(self.temp_path)

    def finish(self):
        self.remove(self.temp_path)

    def execute(self, target: NodePath, action, *arguments):
        return self.backend.execute(target, action, *arguments)
