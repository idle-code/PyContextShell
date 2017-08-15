from contextshell.NodePath import NodePath


class Session:
    def start(self):
        pass

    def finish(self):
        pass

    def execute(self, target: NodePath, action: str, *arguments):
        raise NotImplementedError("Session.execute method was not overridden")

    def get(self, target: NodePath):
        return self.execute(target, 'get')

    def set(self, target: NodePath, new_value):
        return self.execute(target, 'set', new_value)

    def list(self, target: NodePath):
        return self.execute(target, 'list')

    def exists(self, target: NodePath):
        target = NodePath.cast(target)
        return self.execute(target.base_path, 'exists', target.base_name)

    def create(self, target: NodePath, value=None):
        target = NodePath.cast(target)
        return self.execute(target.base_path, 'create', target.base_name, value)

    def remove(self, target: NodePath):
        target = NodePath.cast(target)
        return self.execute(target.base_path, 'remove', target.base_name)
