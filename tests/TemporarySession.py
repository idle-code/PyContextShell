from Session import *


class TemporarySession(Session):
    def __init__(self, underlying_session: Session, temp_path: NodePath):
        self.backend = underlying_session
        self.temp_path = temp_path
        self.start()

    def start(self):
        self.create(self.temp_path)

    def finish(self):
        self.remove(self.temp_path)

    def execute(self, target: NodePath, action, *arguments):
        # Forward all action_tests to the backend
        return self.backend.execute(target, action, *arguments)
