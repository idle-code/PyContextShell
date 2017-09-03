from contextshell.session_stack.SessionLayer import SessionLayer
from contextshell.session_stack.SessionStack import SessionStack
from contextshell.session_stack.StorageLayer import StorageLayer
from contextshell.actions.BasicActions import *


class TreeRoot:
    actions_branch_name = '@actions'

    def __init__(self):
        super().__init__()
        self.root = Node()
        self.root.append(Node(), TreeRoot.actions_branch_name)
        self._install_actions()

    def _install_actions(self):
        self.install_action(GetAction())
        self.install_action(SetAction())
        self.install_action(ListAction())
        self.install_action(ExistsAction())
        self.install_action(CreateAction())
        self.install_action(RemoveAction())

    def install_action(self, action_node: ActionNode):
        if action_node is None:
            raise ValueError("No action to install provided")
        action_path = NodePath.join(TreeRoot.actions_branch_name, action_node.path)
        action_parent = NodePath.create_path(self.root, action_path.base_path)
        action_parent.append(action_node, action_path.base_name)

    def create_session(self) -> SessionStack:
        stack = SessionStack(StorageLayer(self.root))
        return stack
