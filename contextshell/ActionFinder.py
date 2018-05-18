from contextshell.NodePath import NodePath
from contextshell.Tree import Tree

class ActionFinder:
    actions_branch_name = '@actions'

    def __init__(self, tree: Tree):
        self.tree = tree  # TODO: pass tree to the find_action instead?

    def make_action_path(self, target_path: NodePath, action_path: NodePath):
        return NodePath.join(target_path, ActionFinder.actions_branch_name, action_path)

    def find_action(self, target_path: NodePath, action_path: NodePath):
        while True:
            action = self._look_in(target_path, action_path)
            if action is not None:
                return action
            if len(target_path) == 0:
                break
            target_path = target_path.base_path
        return None
        #return self._look_in(self.session_lookup_path, action_path)

    def install_action(self, target_path: NodePath, action_path: NodePath, action):
        self.tree.create(self.make_action_path(target_path, action_path), action)

    def _look_in(self, candidate_path: NodePath, action_name: NodePath):
        candidate_action_path = self.make_action_path(candidate_path, action_name)
        if self.tree.exists(candidate_action_path):
            return self.tree.get(candidate_action_path)
        return None
