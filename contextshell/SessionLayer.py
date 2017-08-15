from contextshell.NodePath import NodePath


class SessionLayer:
    def start(self):
        pass

    def finish(self):
        pass

    def get(self, path: NodePath):
        raise NotImplementedError()

    def set(self, path: NodePath, new_value):
        raise NotImplementedError()

    def list(self, path: NodePath):
        raise NotImplementedError()

    def exists(self, path: NodePath) -> bool:
        raise NotImplementedError()

    def create(self, path: NodePath, value=None):
        raise NotImplementedError()

    def remove(self, path: NodePath):
        raise NotImplementedError()
