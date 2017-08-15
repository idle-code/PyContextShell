from contextshell.NodePath import NodePath


class SessionLayer:
    def __init__(self):
        self.next_layer: 'SessionLayer' = None

    # TODO: use context manager for automatic start/exit
    def start(self, underlying_layer: 'SessionLayer'):
        self.next_layer = underlying_layer

    def finish(self):
        pass

    def get(self, path: NodePath):
        return self.next_layer.get(path)

    def set(self, path: NodePath, new_value):
        return self.next_layer.set(path, new_value)

    def list(self, path: NodePath) -> [str]:
        return self.next_layer.list(path)

    def exists(self, path: NodePath) -> bool:
        return self.next_layer.exists(path)

    def create(self, path: NodePath, value=None):
        return self.next_layer.create(path, value)

    def remove(self, path: NodePath):
        return self.next_layer.remove(path)
