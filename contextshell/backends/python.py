from typing import Any

from ..action import BuiltinExecutor


class PythonObjectTree(BuiltinExecutor):
    def __init__(self, root_object: Any):
        super().__init__()
        if root_object is None:
            raise ValueError("Root object cannot be None")
        self.root_object = root_object
