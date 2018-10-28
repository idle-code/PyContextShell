from typing import Any, List

from ..action import BuiltinExecutor, action_from_function
from ..path import NodePath


class PythonObjectTree(BuiltinExecutor):
    def __init__(self, root_object: Any):
        super().__init__()
        if root_object is None:
            raise ValueError("Root object cannot be None")
        self.root_object = root_object

        self.register_builtin_action(action_from_function(self.contains_action))
        self.register_builtin_action(action_from_function(self.get_action))
        self.register_builtin_action(action_from_function(self.set_action))
        self.register_builtin_action(action_from_function(self.list_action))
        self.register_builtin_action(action_from_function(self.list_actions_action))

    # TODO: try to resolve action to the method if it exists

    @staticmethod
    def _is_field(obj, name: str) -> bool:
        if name.startswith("_"):
            return False
        attribute = getattr(obj, name, None)
        if attribute is None:
            return False
        return not callable(attribute)

    @staticmethod
    def _is_action(obj, name: str) -> bool:
        if name.startswith("_"):
            return False
        attribute = getattr(obj, name)
        return callable(attribute)

    @staticmethod
    def _resolve_to_object(start_obj, path: NodePath):
        current_obj = start_obj
        for part in path:
            if not PythonObjectTree._is_field(current_obj, part):
                return None
            current_obj = getattr(current_obj, part)
        return current_obj

    def contains_action(self, target: NodePath, name: NodePath) -> bool:
        target_obj = self._resolve_to_object(self.root_object, target)
        return self._resolve_to_object(target_obj, NodePath(name)) is not None

    def get_action(self, target: NodePath) -> bool:
        target_obj = self._resolve_to_object(self.root_object, target)
        return target_obj

    def set_action(self, target: NodePath, new_value):
        parent_obj = self._resolve_to_object(self.root_object, target.base_path)
        setattr(parent_obj, target.base_name, new_value)

    def list_action(self, target: NodePath) -> List[NodePath]:
        target_obj = self._resolve_to_object(self.root_object, target)
        return [NodePath(f) for f in dir(target_obj) if self._is_field(target_obj, f)]

    def list_actions_action(self, target: NodePath) -> List[NodePath]:
        target_obj = self._resolve_to_object(self.root_object, target)
        target_actions = [NodePath(f) for f in dir(target_obj) if self._is_action(target_obj, f)]
        builtin_actions = self.list_builtin_actions()

        return target_actions + builtin_actions
