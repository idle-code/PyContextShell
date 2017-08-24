from contextshell.session_stack.SessionLayer import *
from typing import List


class RelativeLayer(SessionLayer):
    """Layer responsible for providing relative navigation in tree"""

    def __init__(self, current_path: NodePath):
        super().__init__()
        self.current = current_path

    # def get(self, path: NodePath):
    #     return self.next_layer.get(path)
    #
    # def set(self, path: NodePath, new_value):
    #     raise NotImplementedError()
    #
    # def list(self, path: NodePath) -> List[NodePath]:
    #     raise NotImplementedError()
    #
    # def exists(self, path: NodePath) -> bool:
    #     raise NotImplementedError()
    #
    # def create(self, path: NodePath, value=None):
    #     raise NotImplementedError()
    #
    # def remove(self, path: NodePath):
    #     raise NotImplementedError()
