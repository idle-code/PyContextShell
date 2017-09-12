from contextshell.NodePath import NodePath
from contextshell.ActionNode import ActionNode
from contextshell.session_stack.SessionLayer import SessionLayer
from contextshell.session_stack.SessionStack import SessionStack
from typing import List


class Session(SessionStack):
    actions_branch_name = '@actions'
    default_action_storage = NodePath('.')

    def __init__(self, storage_layer: SessionLayer):
        super().__init__(storage_layer)

    def install_action(self, action_node: ActionNode, action_path: NodePath = default_action_storage):
        if action_node is None:
            raise ValueError("No action to install provided")
        action_path = NodePath.join(action_path, self.actions_branch_name, action_node.path)
        self.create_path(action_path.base_path)
        self.create(action_path, action_node.get())

    def create_path(self, path: NodePath):
        tested_path = NodePath(absolute=path.is_absolute)
        for name in path:
            tested_path = NodePath.join(tested_path, name)
            if not self.exists(tested_path):
                self.create(tested_path)
    #
    # def _create_temporary_node(self) -> NodePath:
    #     tmp_path = 'tmp'
    #     if not self.root.contains(tmp_path):
    #         self.root.append(Node(), tmp_path)
    #         self.root.get_node(tmp_path).append(Node(0), '@next_id')
    #     tmp_node = self.root.get_node(tmp_path)
    #
    #     next_id = tmp_node.get_node('@next_id').get()
    #     tmp_node.get_node('@next_id').set(next_id + 1)
    #
    #     new_node_name = "tmp{}".format(next_id)
    #     tmp_node.append(Node(), new_node_name)
    #
    #     new_node_path = NodePath.join(tmp_path, new_node_name)
    #     new_node_path.is_absolute = True
    #     return new_node_path
