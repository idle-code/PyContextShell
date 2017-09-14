from contextshell.session_stack.VirtualMappingLayer import VirtualMappingLayer
from contextshell.NodePath import NodePath


class SessionStorageLayer(VirtualMappingLayer):
    session_path: NodePath = NodePath('.session')

    def __init__(self, backing_path: NodePath):  # TODO: use temporary session for backin_path generation
        super().__init__(self.session_path, backing_path)
