from contextshell.actions.BasicActions import *


class TreeRoot(Node):
    actions_branch_name = '@actions'
    default_action_storage = NodePath()

    def __init__(self):
        super().__init__()
        self.append(Node(), TreeRoot.actions_branch_name)
        self._install_actions()

    def _install_actions(self):
        self.install_action(GetAction())
        self.install_action(SetAction())
        self.install_action(ListAction())
        self.install_action(ExistsAction())
        self.install_action(CreateAction())
        self.install_action(RemoveAction())

    def install_action(self, action_node: ActionNode, action_path: NodePath=default_action_storage):
        if action_node is None:
            raise ValueError("No action to install provided")
        action_path = NodePath.join(action_path, self.actions_branch_name, action_node.path)
        action_parent = NodePath.create_path(self, action_path.base_path)
        action_parent.append(action_node, action_path.base_name)
