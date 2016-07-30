from Node import *
from NodePath import *

class Command:
    def __init__(self, target, name, arguments = []):
        self.target = Command._wrap_arg(target)
        self.name = Command._wrap_arg(name)
        self.arguments = list(map(Command._wrap_arg, arguments))

    @staticmethod
    def _wrap_arg(value) -> Node:
        if isinstance(value, Command):
            return value
        if isinstance(value, Node):
            return value # No need to wrap nodes

        if isinstance(value, str):
            # Try parse string as one of supported values
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass # Treat value as text

        return Node(value)

    def __str__(self):
        return "{{{}: {}}}".format(self.target, " ".join([self.name] + self.arguments))

