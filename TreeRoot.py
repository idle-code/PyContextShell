from NodePath import NodePath
from BasicActions import *
from ActionNode import ActionNode
from Session import Session


class TreeRoot(Session):
    actions_branch_name = '@actions'

    def __init__(self):
        super().__init__()
        self.root = Node()
        self.start()

    def start(self):
        self.root.append(Node(), TreeRoot.actions_branch_name)
        actions_node = self.root[TreeRoot.actions_branch_name]
        actions_node.append(ActionNode(BasicActions.get), 'get')
        actions_node.append(ActionNode(BasicActions.set), 'set')
        actions_node.append(ActionNode(BasicActions.list), 'list')
        actions_node.append(ActionNode(BasicActions.exists), 'exists')
        actions_node.append(ActionNode(BasicActions.create), 'create')
        actions_node.append(ActionNode(BasicActions.remove), 'remove')

    def execute(self, target_path: NodePath, action_path: NodePath, *arguments):
        target_node = TreeRoot._resolve(self.root, target_path)
        if target_node is None:
            raise NameError("Target '{}' not found".format(target_path))

        action_node = TreeRoot._find_action(target_node, action_path)
        if action_node is None:
            raise NameError("Action '{}' not found for target path: '{}'".format(action_path, target_path))

        return action_node(target_node, *arguments)

    @staticmethod
    def _find_action(target: Node, action_path: NodePath) -> ActionNode:
        full_action_path = NodePath.join(TreeRoot.actions_branch_name, action_path)
        while target is not None:
            action_node = TreeRoot._resolve(target, full_action_path)
            if action_node is not None:
                return action_node
            target = target.parent
        return None

    @staticmethod
    def _resolve(root: Node, path: NodePath) -> Node:
        path = NodePath.cast(path)
        if path.is_absolute:
            while root.parent is not None:
                root = root.parent
        if len(path) == 0:
            return root
        node = root.get_node(name=path[0])
        if node is None:
            return None
        return TreeRoot._resolve(node, path[1:])
