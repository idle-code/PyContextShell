from typing import Any

from ..action import BuiltinExecutor, action_from_function
from ..path import NodePath


class PythonObjectTree(BuiltinExecutor):
    def __init__(self, root_object: Any):
        super().__init__()
        if root_object is None:
            raise ValueError("Root object cannot be None")
        self.root_object = root_object

        self.register_builtin_action(action_from_function(self.contains_action))

    @staticmethod
    def _resolve_to_object(start_obj, path: NodePath):
        current_obj = start_obj
        for part in path:
            current_obj = getattr(current_obj, part, None)
            if callable(current_obj):
                return None
            if current_obj is None:
                return None
        return current_obj

    def contains_action(self, target: NodePath, name: NodePath) -> bool:
        target_obj = self._resolve_to_object(self.root_object, target)
        assert target_obj
        return self._resolve_to_object(target_obj, NodePath(name)) is not None
