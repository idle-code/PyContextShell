from contextshell.session_stack.SessionLayer import SessionLayer
from contextshell.session_stack.SessionStorageLayer import SessionStorageLayer
from contextshell.Command import Command
from contextshell.NodePath import NodePath


class CommandInterpreter:
    actions_branch_name = '@actions'  # TODO: define in single place (see TreeRoot)
    session_lookup_path = SessionStorageLayer.session_path

    def __init__(self, session: SessionLayer):
        self.session = session

    def execute(self, command: Command):
        target_path = NodePath.cast(self.evaluate(command.target))
        action_path = NodePath.cast(self.evaluate(command.name))
        arguments = map(self.evaluate, command.arguments)
        action = self._find_action(target_path, action_path)
        if action is None:
            raise NameError("Could not find action named '{}'".format(action_path))
        return action(self.session, target_path, *arguments)

    def evaluate(self, part):
        if isinstance(part, Command):
            return self.execute(part)
        return part

    def _find_action(self, target_path: NodePath, action_path: NodePath):
        prefixed_action_path = NodePath.join(CommandInterpreter.actions_branch_name, action_path)
        while True:
            candidate_action_path = NodePath.join(target_path, prefixed_action_path)
            if self.session.exists(candidate_action_path):
                return self.session.get(candidate_action_path)
            if len(target_path) == 0:
                break
            target_path = target_path.base_path

        candidate_action_path = NodePath.join(self.session_lookup_path, prefixed_action_path)
        if self.session.exists(candidate_action_path):
            return self.session.get(candidate_action_path)

        return None
