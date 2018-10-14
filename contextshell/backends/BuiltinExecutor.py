from typing import Optional, List, Dict

from contextshell.backends.ActionExecutor import ActionExecutor, Action
from contextshell.NodePath import NodePath


class BuiltinExecutor(ActionExecutor):
    """Manages built-in, global action registry"""
    def __init__(self):
        super().__init__()
        self.builtin_actions: Dict[NodePath, Action] = {}

    def register_action(self, action: Action):
        if action is None:
            raise ValueError("No action to register provided")
        if action.name in self.builtin_actions:
            raise ValueError(f"Builtin action '{action.name}' already registered")
        self.builtin_actions[action.name] = action

    def list_actions(self) -> List[Action]:
        return list(self.builtin_actions.values())

    def find_action(self, target: NodePath, action: NodePath) -> Optional[Action]:
        return self.builtin_actions.get(action) 
