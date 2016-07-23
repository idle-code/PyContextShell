from Node import *
from NodePath import *

class Command:
    def __init__(self, target, name, arguments = []):
        self.target = self._to_path(target)
        self.name = self._to_path(name)
        self.arguments = arguments

    def _to_path(self, value) -> NodePath:
        if isinstance(value, NodePath):
            return value
        return NodePath(value)

    def __str__(self):
        args = " ".join(map(str, self.arguments))
        if len(args) > 0:
            return "{{{}: {} {}}}".format(self.target, self.name, args)
        else:
            return "{{{}: {}}}".format(self.target, self.name)

