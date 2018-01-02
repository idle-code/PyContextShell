from contextshell.session_stack.Session import Session
from contextshell.Node import Node
from contextshell.NodePath import NodePath
from contextshell.session_stack.StorageLayer import StorageLayer
from contextshell.session_stack.SessionStorageLayer import SessionStorageLayer
from contextshell.session_stack.SessionStack import SessionStack
from contextshell.session_stack.RelativeLayer import *
from contextshell.CommandInterpreter import CommandInterpreter
from contextshell.actions.BasicActions import *


class SessionManager:
    actions_branch_name = '@actions'
    default_action_storage = NodePath()

    def __init__(self, root: Node):
        self.root = root
        self.root.append(Node(), SessionManager.actions_branch_name)
        self._install_builtin_actions(self.create_session())

    def _install_builtin_actions(self, session: Session):
        session.install_action(GetAction())
        session.install_action(SetAction())
        session.install_action(ListAction())
        session.install_action(ExistsAction())
        session.install_action(CreateAction())
        session.install_action(RemoveAction())

    def create_session(self) -> Session:
        session = Session(StorageLayer(self.root))
        session_backend_path = self._create_temporary_node()
        session.push(SessionStorageLayer(session_backend_path))

        # session.install_action(PwdAction(), SessionStorageLayer.session_path)
        # session.install_action(CdAction(), SessionStorageLayer.session_path)
        session.push(RelativeLayer(NodePath('.')))
        return session

    def _create_temporary_node(self) -> NodePath:
        tmp_path = 'tmp'
        if not self.root.contains(tmp_path):
            self.root.append(Node(), tmp_path)
            self.root.get_node(tmp_path).append(Node(0), '@next_id')
        tmp_node = self.root.get_node(tmp_path)

        next_id = tmp_node.get_node('@next_id').get()
        tmp_node.get_node('@next_id').set(next_id + 1)

        new_node_name = "tmp{}".format(next_id)
        tmp_node.append(Node(), new_node_name)

        new_node_path = NodePath.join(tmp_path, new_node_name)
        new_node_path.is_absolute = True
        return new_node_path
